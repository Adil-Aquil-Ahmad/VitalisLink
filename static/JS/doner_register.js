document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();
    
    const bloodGroup = document.querySelector('input[name="blood_group"]').value.trim().toUpperCase();
    const age = parseInt(document.querySelector('input[name="age"]').value, 10);
    const validBloodGroups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"];

    const errorBox = document.getElementById('error-messages');
    errorBox.innerHTML = '';
    errorBox.style.display = 'none';
    errorBox.style.color = '#721c24';
    errorBox.style.backgroundColor = '#f8d7da';
    errorBox.style.border = '1px solid #f5c6cb';
    errorBox.style.padding = '10px';
    errorBox.style.borderRadius = '5px';
    errorBox.style.marginBottom = '15px';

    let errors = [];

    if (isNaN(age) || age < 18) {
        errors.push('You must be at least 18 years old to donate blood.');
    }

    if (!validBloodGroups.includes(bloodGroup)) {
        errors.push('Please enter a valid blood group.');
    }

    if (errors.length > 0) {
        errors.forEach((error) => {
            const errorElement = document.createElement('p');
            errorElement.textContent = error;
            errorElement.style.margin = '5px 0';
            errorBox.appendChild(errorElement);
        });

        errorBox.style.display = 'block';
    } else {
        this.submit();
    }
});
