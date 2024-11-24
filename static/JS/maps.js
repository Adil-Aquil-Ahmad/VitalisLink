function initAutocomplete() {
    const addressInput = document.getElementById('address');
    const autocomplete = new google.maps.places.Autocomplete(addressInput);

    autocomplete.setFields(['address_components', 'geometry']);

    autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace();

        if (place.geometry) {
            document.getElementById('latitude').value = place.geometry.location.lat();
            document.getElementById('longitude').value = place.geometry.location.lng();
        }

        document.querySelector('input[name="city"]').value = '';
        document.querySelector('input[name="state"]').value = '';
        document.querySelector('input[name="pin_code"]').value = '';

        if (place.address_components) {
            place.address_components.forEach(component => {
                const types = component.types;

                if (types.includes('locality')) {
                    // City
                    document.querySelector('input[name="city"]').value = component.long_name;
                } else if (types.includes('administrative_area_level_1')) {
                    // State
                    document.querySelector('input[name="state"]').value = component.long_name;
                } else if (types.includes('postal_code')) {
                    // Pin Code
                    document.querySelector('input[name="pin_code"]').value = component.long_name;
                }
            });
        }
    });
}

window.onload = initAutocomplete;