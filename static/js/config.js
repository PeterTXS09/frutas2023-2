var mousePressed = false;
var lastX, lastY;
var ctx;

function getRndInteger(min, max) {
return Math.floor(Math.random() * (max - min) ) + min;
}

function InitThis() {
  ctx = document.getElementById('myCanvas').getContext("2d");

  numero = getRndInteger(0, 10);
  letra = ["Manzana", "Pera", "Platano"];
  random = Math.floor(Math.random() * letra.length);
  aleatorio = letra[random];

  document.getElementById('mensaje').innerHTML  = 'Dibuja una fruta (Platano, Pera, Manzana)';
  document.getElementById('numero').value = aleatorio;

  $('#myCanvas').mousedown(function (e) {
      mousePressed = true;
      Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, false);
  });

  $('#myCanvas').mousemove(function (e) {
      if (mousePressed) {
          Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, true);
      }
  });

  $('#myCanvas').mouseup(function (e) {
      mousePressed = false;
  });
    $('#myCanvas').mouseleave(function (e) {
      mousePressed = false;
  });
}

function Draw(x, y, isDown) {
  if (isDown) {
      ctx.beginPath();
      ctx.strokeStyle = 'black';
      ctx.lineWidth = 11;
      ctx.lineJoin = "round";
      ctx.moveTo(lastX, lastY);
      ctx.lineTo(x, y);
      ctx.closePath();
      ctx.stroke();
  }
  lastX = x; lastY = y;
}

function clearArea() {
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
}

function prepareImg() {
 var canvas = document.getElementById('myCanvas');
 document.getElementById('myImage').value = canvas.toDataURL();
}