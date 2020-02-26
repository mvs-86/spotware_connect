=====
Usage
=====


Before you begin, follow the Getting Started guide for Open Api 2: https://connect.spotware.com/docs/open_api_2/getting_started_v2


To use spotware_connect in a project::

    import spotware_connect as sc

    c = sc.Client()

    @c.event  # on connect event handler
    def connect():
        c.emit("VersionReq")  # send a ProtoOAVersionReq

        # send a ProtoOAVersionReq with a clientMsgId
        c.emit("VersionReq", msgid="V1")

        # send a ProtoOAApplicationAuthReq with data
        c.emit("ApplicationAuthReq", clientId="YOUR_APP_CLIENT_ID",
               clientSecret="YOUR_APP_CLIENT_SECRET")

    @c.event  # on disconnect event handler
    def disconnect():
        print("Disconencted")

    @c.event  # global message receive handler
    def message(msg, payload, **kargs):  # access ProtoMessage or its payload objects
        print("Global Received message ", repr(msg))
        print("Global Received payload ", repr(payload))

    @c.message(msgtype="ErrorRes")  # handle ProtoOAErrorRes messages
    def on_error(payload, **kargs):
        print("Error: ", repr(payload))
        c.stop()  # stops client

    @c.message(msgtype="VersionRes")  # handle ProtoOAVersionRes messages
    # access version atribute of ProtoOAVersionRes
    def on_version(msg, payload, version, **kargs):
        print("Api Version: ", version)

    @c.message(msgid="V1")  # handle messages with clientMsgId=V1
    def on_version(msg, payload, **kargs):
        print("Received Message with msgid 'V1': ", repr(payload))

    # handle ProtoOAApplicationAuthRes messages
    @c.message(msgtype="ApplicationAuthRes")
    def on_auth_ok(**kargs):
        print("Application Authorized")
        c.stop()  # stops client

    c.start(timeout=5)  # optional: set a timeout interval in seconds


You can find the message types and their params at https://connect.spotware.com/docs/open_api_2/protobuf_messages_reference_v2/open_api_messages
