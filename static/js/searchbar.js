const picture_search = $('#product_search');
const picture_div = document.getElementById('searched_products');
const page_content = document.getElementById('page-content');

let debounceTimer = null;

const currentLang = document.documentElement.lang || 'en';

function renderPicture(picture) {
    let name = currentLang === "uk" ? picture.name_uk : picture.name_en;

    return `
        <div class="my_card">
          <a href="/picture_details/${picture.id}/" class="invisible-link">
            <div class="row g-2 align-items-start">
              <div class="col-6">
                <img src="${picture.presigned_url}" alt="${name}" style="max-width:300px;">
              </div>
              <div class="col-6 text-start">
                <h4>Short Picture Info:</h4>
                <span class="badge badge_text bg-warning text-dark">
                    Picture name: ${name}
                </span><br>
                <span class="badge badge_text bg-warning text-dark">
                    Size: ${picture.sizeHorizontal} x ${picture.sizeVertical} cm
                </span><br>
                <span class="badge badge_text bg-warning text-dark">
                    Price: ${picture.price} £
                </span><br>
              </div>
            </div>
          </a>
        </div>
    `;
}

picture_search.on('input', () => {
    clearTimeout(debounceTimer);

    debounceTimer = setTimeout(() => {
        const search_word = picture_search.val().trim();
        if (!search_word) {
            picture_div.innerHTML = '';
            picture_div.classList.add('d-none');
            page_content.classList.remove('d-none');
            return;
        }

        $.getJSON('/product-search/', { search_word: search_word }, (pictures) => {
            picture_div.innerHTML = '';
            if (pictures.length > 0) {
                page_content.classList.add('d-none');
                picture_div.classList.remove('d-none');

                pictures.forEach(picture => {
                    picture_div.innerHTML += renderPicture(picture);
                });
            } else {
                page_content.classList.add('d-none');
                picture_div.classList.remove('d-none');
                picture_div.innerHTML = `<h4>No results found ...</h4>`;
            }
        });
    }, 500);
});