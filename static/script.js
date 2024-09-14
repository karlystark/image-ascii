document.getElementById('upload-form').addEventListener('submit', async (event) => {
  event.preventDefault();

  const formData = new FormData();
  const fileData = document.getElementById('image-input').files[0];

  if(!fileData){
    console.log('no file data');
    return;
  }

  console.log(fileData);

  formData.append('image', fileData);


  try {
      const response = await fetch('http://localhost:5001/convert', {
          method: 'POST',
          body: formData,
      });

      const asciiArt = await response.text();
      document.getElementById('ascii-output').innerText = asciiArt;
  } catch (error) {
      console.error('Error:', error);
  }
});
