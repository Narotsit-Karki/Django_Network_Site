

  document.getElementById("video_1").onchange = function(event){
  let file_1 = event.target.files[0];
  let blobURL_1 = URL.createObjectURL(file_1);
  document.getElementById("photo_1").value = "";
  document.querySelector("#photo_upload_1").style.display = 'none';
  document.querySelector("#video_upload_1").style.display = 'block';
  document.querySelector("#cancel_post").style.display = 'inline-block';
  document.querySelector("#video_upload_1").src = blobURL_1;
   }

  document.getElementById("photo_1").onchange = function(event){
  let file = event.target.files[0];
  let blobURL = URL.createObjectURL(file);
  document.getElementById("video_1").value = "";
  document.querySelector("#video_upload_1").src = '#';
  document.querySelector("#video_upload_1").style.display = 'none';
  document.querySelector("#photo_upload_1").style.display = 'block';
  document.querySelector("#cancel_post").style.display = 'inline-block';
  document.querySelector("#photo_upload_1").src = blobURL;
   }

