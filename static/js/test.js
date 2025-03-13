function getSupportedMimeTypes(media, types, codecs) {
  const isSupported = MediaRecorder.isTypeSupported;
  const supported = [];
  types.forEach((type) => {
    const mimeType = `${media}/${type}`;
    codecs.forEach((codec) => [
        `${mimeType};codecs=${codec}`,
        `${mimeType};codecs=${codec.toUpperCase()}`,
      ].forEach(variation => {
        if(isSupported(variation))
            supported.push(variation);
    }));
    if (isSupported(mimeType))
      supported.push(mimeType);
  });
  return supported;
};

// Usage ------------------
const videoTypes = ["webm", "ogg", "mp4", "x-matroska"];
const audioTypes = ["webm", "ogg", "mp3", "x-matroska"];
const codecs = ["should-not-be-supported","vp9", "vp9.0", "vp8", "vp8.0", "avc1", "av1", "h265", "h.265", "h264", "h.264", "opus", "pcm", "aac", "mpeg", "mp4a"];

const supportedVideos = getSupportedMimeTypes("video", videoTypes, codecs);
const supportedAudios = getSupportedMimeTypes("audio", audioTypes, codecs);

//console.log('-- All supported Videos : ', supportedVideos)
console.log('-- All supported Audios : ', supportedAudios)

/***
 Reproduce un fichero de audio; teóricamente hasta que finaliza
*/
let audio = new Audio();
function playAudio(opcio) {
   function audioPlay() {
      if (!opcio) {
         audio.removeEventListener('ended', audioPlay);
         return;
      }
      audio.src = "static/tmp/temp.wav";
      audio.play();
   }
   audio.addEventListener('ended', audioPlay);
   audioPlay();
}

