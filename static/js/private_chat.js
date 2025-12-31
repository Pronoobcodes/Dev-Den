(function(){
  const username = window.__PRIVATE_CHAT_USERNAME;
  const chatBox = document.getElementById('chat-box');
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  if(!username) return;

  const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
  const wsPath = `${protocol}://${window.location.host}/ws/pm/${username}/`;
  const socket = new WebSocket(wsPath);
  const notificationSocket = new WebSocket(
    `${protocol}://${window.location.host}/ws/notifications/`
  );

  socket.onopen = function(){
    console.log('Private chat websocket opened', wsPath);
  };

  socket.onmessage = function(e){
    try{
      const data = JSON.parse(e.data);
      alert(`🔔 ${data.sender}: ${data.message}`);
      const div = document.createElement('div');
      const sender = data.sender;
      div.className = 'chat-message';
      if(sender === window.__USERNAME) div.classList.add('from-me'); else div.classList.add('from-them');
      div.innerHTML = `<strong>${sender}</strong>: ${data.message}`;
      chatBox.appendChild(div);
      chatBox.scrollTop = chatBox.scrollHeight;
    }catch(err){ console.error(err); }
  };

  socket.onclose = function(){ console.log('chat socket closed'); };

  // fallback to regular POST submit
  chatForm.addEventListener('submit', function(ev){
    ev.preventDefault();
    const val = chatInput.value.trim();
    if(!val) return;
    // try send via websocket first
    if(socket.readyState === WebSocket.OPEN){
      socket.send(JSON.stringify({message: val}));
      chatInput.value = '';
      return;
    }
    chatForm.submit();
  });
})();
