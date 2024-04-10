for (const slider of document.getElementsByClassName('slider')) {
    sliderInit(slider);
}

/**
 * @param {HTMLElement} slider
 */
function sliderInit(slider) {
    const photos_wrapper = slider.querySelector('.slider_photos');
    const photos = photos_wrapper.getElementsByClassName('slider_photo');
    const count = photos.length;

    for (let i = 0; i < count; i++) {
        photos[i].querySelector('.slider_counter').textContent = (i+1)+"/"+count;
        photos[i].hidden = true;
    }

    let cur = 0;
    photos[cur].hidden = false;

    const left = slider.querySelector('.slider_left');
    const right = slider.querySelector('.slider_right');

    left.addEventListener('click', () => {
        photos[cur].hidden = true;
    
        if (cur > 0) cur--;
        else cur = count - 1;
    
        photos[cur].hidden = false;
    });
    
    right.addEventListener('click', () => {
        photos[cur].hidden = true;
    
        if (cur < count - 1) cur++;
        else cur = 0;
    
        photos[cur].hidden = false;
    });
}