;(function () {
    'use strict';
    var socket, domInput, domStream;

    function createMessageDOM(text) {
        var line;
        line = document.createElement('p');
        line.appendChild(document.createTextNode(text));
        return line;
    }

    function showMsg(msg) {
        domStream.insertBefore(createMessageDOM(msg), domStream.firstChild);
    }

    function showAllMsgs(msgs) {
        var i, domStreamNew;
        for (i = 0; i < msgs.length; ++i) {
            showMsg(msgs[i]);
        }
    }

    function sendMessage(msg) {
        socket.emit('send-msg', msg);
    }

    function onSubmit(evt) {
        if (domInput && domInput.value != '') {
            sendMessage(domInput.value);
            domInput.value = '';
        }
        evt.preventDefault();
        return false;
    }

    function initSocketIO() {
        socket = io.connect('//' + document.domain + ':' + location.port);
        socket
        .on('show-msg', showMsg)
        .on('show-all-msgs', showAllMsgs)
        .on('connect', function() {
            socket.emit('request-all-msgs');
        });
    }

    function onDOMContentLoaded(evt) {
        var domInputForm = document.getElementById('inputForm')
        domInputForm.addEventListener('submit', onSubmit, false);
        domInput = document.getElementById('input');
        domStream = document.getElementById('stream');

        initSocketIO();
    }

    document.addEventListener('DOMContentLoaded', onDOMContentLoaded, false);
})();
