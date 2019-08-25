// Function for tabbing
function openTab(evt, tabName) {
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}


// Function to copy image gallery link to clipboard
function copyText(id) {
    var txtid = "filepath-" + id;
    var copyText = document.getElementById(txtid);

    // Create dummy textare
    var temp = document.createElement("textarea");
    document.body.appendChild(temp);
    temp.value= copyText.innerHTML
    temp.select();

    try {
        document.execCommand('copy');
    } catch (err) {
        console.log('Copy to clipboard was unsuccessful');
    }
}
