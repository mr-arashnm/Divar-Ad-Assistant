
// Handle radio card selection
document.querySelectorAll('.radio-card').forEach(card => {
    card.addEventListener('click', function() {
        document.querySelectorAll('.radio-card').forEach(c => {
            c.classList.remove('selected', 'border-blue-500');
        });
        this.classList.add('selected', 'border-blue-500');
    });
});

// Handle file upload hover states
document.querySelectorAll('.file-upload').forEach(upload => {
    const fileInput = upload.querySelector('input[type="file"]');
    
    upload.addEventListener('click', function() {
        fileInput.click();
    });
    
    upload.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('border-blue-500', 'bg-blue-50');
    });
    
    upload.addEventListener('dragleave', function() {
        this.classList.remove('border-blue-500', 'bg-blue-50');
    });
    
    upload.addEventListener('drop', function(e) {
        e.preventDefault();function generateAd() {
    document.getElementById('step2').classList.add('hidden');
    document.getElementById('resultsSection').classList.remove('hidden');

    // Simulate processing delay
    setTimeout(() => {
        document.getElementById('loadingState').classList.add('hidden');
        document.getElementById('resultsContent').classList.remove('hidden');
    }, 2500);
}
        this.classList.remove('border-blue-500', 'bg-blue-50');
        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            // Here you would handle the file
        }
    });
});

// Navigation functions
function showStep1() {
    document.getElementById('step2').classList.add('hidden');
    document.getElementById('step1').classList.remove('hidden');
}

function showStep2() {
    const inputType = document.querySelector('input[name="inputType"]:checked').value;

    // Hide all forms
    document.getElementById('manualForm').classList.add('hidden');
    document.getElementById('excelForm').classList.add('hidden');
    document.getElementById('imageForm').classList.add('hidden');

    // Show selected form
    document.getElementById(`${inputType}Form`).classList.remove('hidden');

    document.getElementById('step1').classList.add('hidden');
    document.getElementById('step2').classList.remove('hidden');
}

async function generateAd() {
    document.getElementById('step2').classList.add('hidden');
    document.getElementById('resultsSection').classList.remove('hidden');

    const inputType = document.querySelector('input[name="inputType"]:checked').value;
    const formData = {}
    formData.type = inputType
    let path = '';

    if (inputType === 'manual') {
        const category = document.getElementById('productCategory').value;
        const name = document.getElementById('productName').value;
        formData.category = category;
        formData.title = name;
        path = 'http://127.0.0.1:8000/api/get-specs/'
    } else if (inputType === 'image') {
          const fileInput = document.getElementById('productImageUrl').value;
          formData.url = fileInput
          path = 'http://127.0.0.1:8000/api/image-specs/'


    } else if (inputType === 'excel') {
        const excelFile = document.getElementById('excelFile').files[0];
        if (!excelFile) return alert("Please select an Excel file.");
        formData.append('file', excelFile);
    }

   try {
    const response = await fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': '*/*' },
      body: JSON.stringify(formData)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // 1) Read the raw text
    const text = await response.text();

    // 2) Parse JSON only inside its own try/catch
    let result;
    try {
      result = JSON.parse(text);
      // const data = await result.json();
        localStorage.setItem('productData', JSON.stringify(result));
        window.location.href = 'product.html';


        // Display the result on the page
        document.getElementById('loadingState').classList.add('hidden');
        document.getElementById('resultsContent').classList.remove('hidden');
        document.getElementById('resultsContent').innerText = JSON.stringify(result, null, 2);
    } catch (parseErr) {
      console.error('Failed to parse JSON:', parseErr);
      console.error('Server response was:', text);
      alert('Server returned invalid JSON. See console for details.');
      return;
    }



} catch (error) {
    console.error('Error sending request:', error);
    alert('There was a problem communicating with the server!');
}

}


function resetForm() {
    document.getElementById('resultsSection').classList.add('hidden');
    document.getElementById('loadingState').classList.remove('hidden');
    document.getElementById('resultsContent').classList.add('hidden');
    showStep1();
}
