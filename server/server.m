clear;
close all;

global store;
global handlers;
global conn_to_proxy;
global serv_bt_client_server;
global serv_bt_proxy_server;
global elevated;

elevated = false;


% initialize and print the store.
store = containers.Map();
init_store();
print_store();


handlers = containers.Map();
handlers('GET') = @get_hn;
handlers('SET') = @set_hn;
handlers('RESET') = @reset_hn;
handlers('EVICT') = @evict_hn;

handlers('DIRTY') = @dirty_hn;


% initialize the servers and listen them
serv_bt_client_server = init_server(8080);
serv_bt_proxy_server = init_server(8081);

while true
    listen_client(serv_bt_client_server);
    pause(0.1)
    listen_proxy(serv_bt_proxy_server);
    pause(0.1)
    pause(1)
end


%%% FUNCTIONS %%%
function TCPIPServer = init_server(port)
try
    fprintf('Creating server socket... \n');
    TCPIPServer = tcpserver('127.0.0.1', port);
    fprintf('Server CREATED at port %d \n', port);
catch ME
    fprintf('Failed to create server on port %d. Error: %s\n', port, ME.message);
    TCPIPServer = [];
end
end



function listen_client(srv)
global handlers;
if srv.NumBytesAvailable ~= 0
    data = read(srv, srv.NumBytesAvailable, "string");


    [action, params] = Request_Parser(data);

    who = "client";

    handler_func = handlers(action);
    rep = handler_func(params, who);

    reply(srv,rep)
end
end


function listen_proxy(srv)
global conn_to_proxy;
global handlers;
global elevated;

if srv.NumBytesAvailable ~= 0
    data = read(srv, srv.NumBytesAvailable, "string");


    if data == "AUTH SECRET_123;"
        elevated = true;
        conn_to_proxy = srv;
        reply(srv, "AUTH OK;");
    elseif elevated == true

        [action, params] = Request_Parser(data);

        who = "proxy";

        handler_func = handlers(action);
        rep = handler_func(params, who);

        if (rep ~= "ACK")
            reply(srv, rep)
        end

    else
        reply(srv, "NOT_AUTHORIZED;")
        elevated = false;
    end

end

end



function reply(srv, packet)
while (1)
    try
        disp(packet);
        srv.write(packet);
        break;
    catch
        pause(0.1);
    end
end
end






%% REQUEST PARSER %%%
function [action, params] = Request_Parser(raw_data)
splitted_data = split(raw_data, {';', ' ', '='});
switch splitted_data(1)
    case "GET"
        action = "GET";
        params = [split(splitted_data(3), ',')];
    case "SET"
        action = "SET";
        params = [split(splitted_data(3), ',') split(splitted_data(5), ',')];
    case "RESET"
        action = "RESET";
        if length(splitted_data) > 2
            params = splitted_data(3);
        else
            params = "";
        end

    case "EVICT"
        action = "EVICT";
        if length(splitted_data) > 2
            params = splitted_data(3);
        else
            params = "";
        end
    case "DIRTY"
        action = "DIRTY";
        if splitted_data(2) == "OK";
            params = false;
        else
            params = true;
        end

    otherwise
        disp('Invalid command')
end
end


%% HANDLERS %%%
function repl = get_hn(inds, who)
items = strings(0);

for i = 1:length(inds)
    item = get_item_at(inds(i));
    if ~isnan(item)
        items(end+1) = string(item);
    end
end

inds = string(inds);

if length(items) > 0
    print_store();
    repl = sprintf("OK IND=%s DATA=%s;", strjoin(inds, ','), strjoin(items, ','));
else
    print_store();
    repl = "NOT_FOUND";
end
end


function repl = set_hn(params, who)
global conn_to_proxy;

inds = params(:, 1);
data = params(:, 2);

for i = 1:length(inds)
    set_item_at(inds(i), data(i));
end

print_store();
repl = sprintf("OK;");

if who == "client"
    prox_req = sprintf("DIRTY IND=%s;", strjoin(inds, ','));

    if isempty(conn_to_proxy)
        disp("conn_to_proxy is empty");
    else
        reply(conn_to_proxy, prox_req);
    end
end

end


function repl = reset_hn(params, who)
global conn_to_proxy;


if params(1) == ""
    reset_store("");
else
    reset_store(params(1));
end

print_store();
repl = sprintf("OK;");

if who == "client"
    if isempty(conn_to_proxy)
        disp("conn_to_proxy is empty");
    else
        reply(conn_to_proxy, "DIRTY;")
    end
end

end




function repl = dirty_hn(params, who)
global conn_to_proxy;

repl = "ACK";

end



% no effect on server
function repl = evict_hn(params, who)
global conn_to_proxy;

if isempty(conn_to_proxy)
    disp("conn_to_proxy is empty");
else
    reply(conn_to_proxy, "DIRTY;")
end

repl = sprintf("OK;");
end



%% Store Operations %%
function store =init_store()
global store
keys = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};
values = {'Data0', 'Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7', 'Data8', 'Data9'};

store = containers.Map(keys, values);
end

function item =get_item_at(key)
global store
if isKey(store, key)
    item = store(key);
else
    item = NaN;
end
end


function set_item_at(key, value)
global store
store(key) = value;
end

function reset_store(data)
global store
keys = store.keys();
for i = 1:length(keys)
    store(keys{i}) = data;
end
end

function print_store()
global store
keys = store.keys();
values = store.values();
fprintf("+---------------------------------+\n");
fprintf("|          STORE at SERVER        |\n");
fprintf("+---------------------------------+\n");
fprintf("|    Key       |    Value         |\n");
fprintf("+---------------------------------+\n");

for i = 1:length(keys)
    fprintf("|    %s        |     %s       |\n", keys{i}, values{i});
end
end