var fileSize = 0;
var numLines = 1;
var scopeArray = new Int16Array(256); //master
var scopeArray2 = new Int16Array(2); //modules
var animID = null;
var urlPars = {};
var playStatus = 0;
var centerReq = 0;
var offsetX = 0;
var offsetY = 0;
function status(s) {
  // document.getElementById('status').innerHTML = s;
  console.log(s);
}
function info() {
  //Show song information:
  var s = 'File info:<br>';
  s += 'size: ' + fileSize + ' bytes;<br>';
  s += 'name: ' + sv_get_song_name(0) + ';<br>';
  s += 'BPM (Beats Per Minute): ' + sv_get_song_bpm(0) + ';<br>';
  s += 'TPL (Ticks Per Line or Tempo): ' + sv_get_song_tpl(0) + ';<br>';
  s += 'number of frames: ' + sv_get_song_length_frames(0) + ';<br>';
  numLines = sv_get_song_length_lines(0);
  s += 'number of lines: ' + numLines + ';<br>';
  var mm = sv_get_number_of_modules(0);
  s += 'number of modules: ' + mm + ';<br>';
  var pp = sv_get_number_of_patterns(0);
  s += 'number of patterns: ' + pp + ';<br>';
  s += '<pre>Log:\n' + sv_get_log(1024) + '</pre>';
  // document.getElementById('info').innerHTML = s;
  console.log(s);
  info_gfx();
}
function info_gfx() {
  //Draw song information on canvas:
  var canvas = document.getElementById('gfx');
  if (canvas.getContext) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    var ctx = canvas.getContext('2d');
    //
    // Draw modules:
    //
    var mm = sv_get_number_of_modules(0);
    var module_size = 20;
    ctx.textBaseline = 'middle';
    ctx.textAlign = 'center';
    if (animID == null) ctx.strokeStyle = 'white';
    else ctx.strokeStyle = 'rgba(255,255,255,0.5)';
    ctx.fillStyle = '#506070';
    ctx.fillRect(0, 0, canvas.clientWidth, canvas.clientHeight);
    if (centerReq == 1) {
      var x1 = -1000000;
      var y1 = -1000000;
      var x2 = 1000000;
      var y2 = 1000000;
      for (var i = 0; i < mm; i++) {
        var flags = sv_get_module_flags(0, i);
        if ((flags & SV_MODULE_FLAG_EXISTS) == 0) continue;
        var xy = sv_get_module_xy(0, i);
        var x = xy & 0xffff;
        if (x & 0x8000) x -= 0x10000;
        var y = (xy >> 16) & 0xffff;
        if (y & 0x8000) y -= 0x10000;
        if (x > x1) x1 = x;
        if (x < x2) x2 = x;
        if (y > y1) y1 = y;
        if (y < y2) y2 = y;
      }
      offsetX = 512 - (x1 + x2) / 2;
      offsetY = 512 - (y1 + y2) / 2;
      centerReq = 0;
    }
    for (var i = 0; i < mm; i++) {
      var flags = sv_get_module_flags(0, i);
      if ((flags & SV_MODULE_FLAG_EXISTS) == 0) continue;
      var color = sv_get_module_color(0, i);
      var xy = sv_get_module_xy(0, i);
      var x = xy & 0xffff;
      if (x & 0x8000) x -= 0x10000;
      var y = (xy >> 16) & 0xffff;
      if (y & 0x8000) y -= 0x10000;
      x += offsetX;
      y += offsetY;
      x = (x * canvas.clientWidth) / 2056 + 256;
      y = (y * canvas.clientHeight) / 2056 + 256;
      var r = color & 255;
      var g = (color >> 8) & 255;
      var b = (color >> 16) & 255;
      var outputs = sv_get_module_outputs(0, i); //Int32Array with output links (module numbers)
      if (outputs != null) {
        for (var l = 0; l < outputs.length; l++) {
          var i2 = outputs[l];
          if (i2 < 0) continue;
          var xy2 = sv_get_module_xy(0, i2);
          var x2 = xy2 & 0xffff;
          if (x2 & 0x8000) x2 -= 0x10000;
          var y2 = (xy2 >> 16) & 0xffff;
          if (y2 & 0x8000) y2 -= 0x10000;
          x2 += offsetX;
          y2 += offsetY;
          x2 = (x2 * canvas.clientWidth) / 2056 + 256;
          y2 = (y2 * canvas.clientHeight) / 2056 + 256;
          ctx.beginPath();
          ctx.moveTo(x, y);
          ctx.lineTo(x2, y2);
          ctx.stroke();
        }
      }
      var alpha;
      var module_size2;
      if (animID == null) {
        alpha = 0.8;
        module_size2 = module_size;
      } else {
        sv_get_module_scope2(0, i, 0, scopeArray2, 2);
        alpha = Math.abs(scopeArray2[0] / 32768);
        module_size2 = module_size * (1 + alpha / 2);
        alpha += 0.3;
      }
      ctx.fillStyle = 'rgba(' + r + ',' + g + ',' + b + ',' + alpha + ')';
      ctx.fillRect(
        x - module_size2 / 2,
        y - module_size2 / 2,
        module_size2,
        module_size2
      );
      ctx.fillStyle = 'rgba(255,255,255,' + alpha + ')';
      ctx.fillText(sv_get_module_name(0, i), x, y);
    }
    //
    // Draw waveform of the Output module (0):
    //
    if (animID != null) {
      ctx.strokeStyle = 'white';
      var len = scopeArray.length; //number of samples to read
      len = sv_get_module_scope2(0, 0, 0, scopeArray, len);
      if (len > 0) {
        ctx.beginPath();
        ctx.moveTo(-1, canvas.clientHeight / 2);
        for (var i = 0; i < len; i++) {
          var x = (i * canvas.clientWidth) / (len - 1);
          var y =
            canvas.clientHeight / 2 -
            (scopeArray[i] / 32768 / 2) * (canvas.clientHeight / 2);
          ctx.lineTo(x, y);
        }
        ctx.stroke();
      }
      //
      // Draw play position (time):
      //
      ctx.fillStyle = 'white';
      ctx.fillRect(
        1,
        1,
        ((canvas.clientWidth - 2) * sv_get_current_line(0)) / numLines,
        4
      );
    }
  }
}
function loadFromArrayBuffer(buf) {
  if (buf) {
    var byteArray = new Uint8Array(buf);
    if (sv_load_from_memory(0, byteArray) == 0) {
      centerReq = 1;
      fileSize = byteArray.byteLength;
      status('song loaded');
      info();
      if (playStatus) {
        sv_play_from_beginning(0);
      }
    } else {
      status('song load error');
    }
  }
}
function load(fname) {
  status('loading "' + fname + '" ...');
  var req = new XMLHttpRequest();
  req.open('GET', fname, true);
  req.responseType = 'arraybuffer';
  req.onload = function (e) {
    if (this.status != 200) {
      status('file not found');
      return;
    }
    var arrayBuffer = this.response;
    loadFromArrayBuffer(arrayBuffer);
  };
  req.send(null);
}
function anim() {
  if (animID == null) {
    animID = window.setInterval(info_gfx, 1000 / 15);
  } else {
    window.clearInterval(animID);
    animID = null;
    info();
  }
}
//Get URL parameters:
var v = window.location.search.slice(1).split('&');
for (var i = 0; i < v.length; i++) {
  var pair = v[i].split('=');
  urlPars[pair[0]] = pair[1];
}
//File button:
function fileChanged(evt) {
  var file = evt.target.files[0];
  var reader = new FileReader();
  reader.onloadend = function () {
    status('loading...');
    loadFromArrayBuffer(reader.result);
  };
  if (file) reader.readAsArrayBuffer(file);
}
//Start SunVox:
svlib.then(function (Module) {
  //
  // SunVox Library was successfully loaded.
  // Here we can perform some initialization:
  //
  svlib = Module;
  status('SunVoxLib loading is complete');
  var ver = sv_init(0, 44100, 2, 0); //Global sound system init
  if (ver >= 0) {
    //Show information about the library:
    var major = (ver >> 16) & 255;
    var minor1 = (ver >> 8) & 255;
    var minor2 = ver & 255;
    console.log('SunVox lib version: ' + major + ' ' + minor1 + ' ' + minor2);
    status('init ok');
  } else {
    status('init error');
    return;
  }
  sv_open_slot(0); //Open sound slot 0 for SunVox; you can use several slots simultaneously (each slot with its own SunVox engine)
  //
  // Try to load and play some SunVox file:
  //
  var fname = 'music/NightRadio - machine 0001.sunvox';
  if (urlPars['file'] != null) fname = decodeURIComponent(urlPars['file']);
  anim();
  load(fname);
});
