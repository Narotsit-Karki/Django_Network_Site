<script>
  document.getElementById("updateProfilePicInput_1").onchange = function(event){
  let file = event.target.files[0];
  let blobURL = URL.createObjectURL(file);
  document.querySelector("#profile_update").style.display = 'none';
  document.querySelector("#update_button_group").style.display = 'block';
  document.querySelector("#profile_background").src = blobURL;
  }

  document.getElementById("updateProfilePicInput_2").onchange = function(event){
  let file = event.target.files[0];
  let blobURL = URL.createObjectURL(file);
  document.querySelector("#update_profile_pic").style.display = 'none';
  document.querySelector("#update_button_group_1").style.display = 'block';
  document.querySelector("#profile_pic").src = blobURL;
  }

</script>