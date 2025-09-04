const pictureSearch = $('#product_search');
const pictureDiv = document.getElementById('searched_products');
const pageContent = document.getElementById('page-content');

let debounceTimer = null;
const currentLang = document.documentElement.lang || 'en';

function renderPicture(picture) {
    const name = currentLang === "uk" ? picture.name_uk : picture.name_en;

    return `
        <div class="col">
            <a href="/picture_details/${picture.id}/" class="text-decoration-none">
                <div class="card shadow-sm">
                    <img src="${picture.presigned_url}" class="bd-placeholder-img card-img-top"
                         alt="${name}" height="250" style="object-fit: cover; width: 100%;">
                    <div class="card-body">
                        <h4 class="card-title">Short Picture Info:</h4>
                        <span class="badge bg-warning text-dark">Picture name: ${name}</span><br>
                        <span class="badge bg-warning text-dark">
                            Size: ${picture.sizeHorizontal} x ${picture.sizeVertical} cm
                        </span><br>
                        <span class="badge bg-warning text-dark">Price: ${picture.price} £</span>
                    </div>
                </div>
            </a>
        </div>
    `;
}

pictureSearch.on('input', () => {
    clearTimeout(debounceTimer);

    debounceTimer = setTimeout(() => {
        const searchWord = pictureSearch.val().trim();

        if (!searchWord) {
            pictureDiv.innerHTML = '';
            pictureDiv.classList.add('d-none');
            pageContent.classList.remove('d-none');
            return;
        }

        $.getJSON('/product-search/', { search_word: searchWord }, (pictures) => {
            pictureDiv.innerHTML = '';

            if (pictures.length > 0) {
                pageContent.classList.add('d-none');
                pictureDiv.classList.remove('d-none');

                pictures.forEach(picture => {
                    pictureDiv.innerHTML += renderPicture(picture);
                });
            } else {
                pageContent.classList.add('d-none');
                pictureDiv.classList.remove('d-none');
                pictureDiv.innerHTML = `<
