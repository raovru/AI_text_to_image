console.log('JavaScript file loaded');

const form = document.querySelector('#text-form');
const submitButton = document.querySelector('#submit-button');
const resultImageBox = document.querySelector('#result-image-box');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    submitButton.disabled = true;
    submitButton.classList.add("submit-button--loading");

    const formData = new FormData(form);

    try {
        const response = await axios.post('http://localhost:8000/textToImage', formData);
        
        if (response.data.image) {
        resultImageBox.innerHTML = `<img src="data:image/jpeg;base64,${response.data.image}" alt="Generated Image"/>`;
        } else {
        resultImageBox.innerHTML = "<p>Error generating image</p>";
        }
    } 
    catch (error) {
        resultImageBox.innerHTML = "<p>Error generating image</p>";
        console.error('There was a problem with the fetch operation:', error);
    } 
    finally {
        submitButton.disabled = false;
        submitButton.classList.remove('submit-button--loading');
    }
});