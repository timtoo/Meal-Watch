google.load('search', '1');

var imageSearch;

function searchComplete() {

  // Check that we got results
  if (imageSearch.results && imageSearch.results.length > 0) {

    // Grab our content div, clear it.
    var contentDiv = document.getElementById('google-images');
    contentDiv.innerHTML = '';

    // Loop through our results, printing them to the page.
    var results = imageSearch.results;
    for (var i = 0; i < Math.min(4, results.length); i++) {

      var result = results[i];
      var imgContainer = document.createElement('div');
      var aContainer = document.createElement('a');
      var newImg = document.createElement('img');

      aContainer.title = result.titleNoFormatting;
      aContainer.href = result.originalContextUrl;
      newImg.src=result.tbUrl;
      newImg.height='100';

      aContainer.appendChild(newImg);
      imgContainer.style.cssFloat = "left";
      imgContainer.appendChild(aContainer);

      contentDiv.appendChild(imgContainer);
    }

  }
}

function OnLoad() {

  imageSearch = new google.search.ImageSearch();
  imageSearch.setSearchCompleteCallback(this, searchComplete, null);
  imageSearch.execute(image_search_terms);
  //google.search.Search.getBranding('branding');

}
google.setOnLoadCallback(OnLoad);

