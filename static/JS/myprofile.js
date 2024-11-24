document.addEventListener('DOMContentLoaded', () => {
    const editButton = document.querySelector('.edit-btn');
    const saveButton = document.querySelector('.save-btn');
    const inputs = document.querySelectorAll('#address, #city, #state, #pin_code, #blood_group, #first_name, #middle_name, #last_name, #age');

    editButton.addEventListener('click', () => {
        inputs.forEach(input => {
            input.removeAttribute('readonly');
            input.style.background = "#fff";
            input.style.border = "1px solid #951a1a";
        });
        editButton.style.display = 'none';
        saveButton.style.display = 'block';
    });
});
