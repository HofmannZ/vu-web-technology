// Renders one product to the DOM.
function renderInventoryItem(inventoryItem, productInventoryList) {
  // Calculate the seccond last position in the table and insert a new row.
  var position = productInventoryList.querySelectorAll('tr').length - 1;
  var row = productInventoryList.insertRow(position);

  // Create the table celss for the product.
  var name = row.insertCell(-1);
  var category = row.insertCell(-1);
  var amount = row.insertCell(-1);
  var location = row.insertCell(-1);
  var date = row.insertCell(-1);

  // Fill the cells with the product data.
  name.innerHTML = inventoryItem.name;
  category.innerHTML = inventoryItem.category;
  amount.innerHTML = inventoryItem.amount;
  location.innerHTML = inventoryItem.location;
  date.innerHTML = inventoryItem.date;
};

// Renders a n amount of products to the DOM.
function renderInventory(productInventory) {
  // Get the product inventory list as a DOM element.
  var productInventoryList = document.querySelector('.product-inventory__list');

  // While there are still products in the list remove them.
  while (productInventoryList.querySelectorAll('tr').length > 1) {
    productInventoryList.deleteRow(0);
  };

  // For each item in the productInventory render it.
  for (var i = 0; i < productInventory.length; i++) {
    renderInventoryItem(productInventory[i], productInventoryList);
  };
};

// Some custom boilerplate for the AJAX request.
function ajaxRequest(method, url, data, callback) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState === 4 && (this.status === 200 || this.status === 201)) {
      // If there is a good resopens return it to the callback as a JavaScript object.
      callback(JSON.parse(this.responseText));
    } else if (this.readyState === 4) {
      // If there is a error return an error object as the seccond argument for the callback.
      callback(null, {
        code: this.status,
        message: 'An error has ocured.',
      });
    }
  };

  // Open the AJAX request.
  xhttp.open(method, url, true);

  if (data) {
    // If there is data add the right request header and send the request with data.
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.send(data);
  } else {
    // Else just sent the request.
    xhttp.send();
  }
};

function fetchInventory(callback) {
  ajaxRequest('GET', 'http://wt.ops.few.vu.nl/api/9ca8e4fc', false, function(response, error) {
    if (error) {
      // If an error ocures send it to the console.
      console.error(error.code, error.message);
    } else if (response) {
      // If we get a resonse execute the callback function with that response.
      callback(response);
    }
  });
};

function populateInventory() {
  // Fetch the current product inventory from the API.
  fetchInventory(function(productInventory) {
    // Render the current product inventory to the DOM.
    renderInventory(productInventory);
  });
};

function addInventoryItem() {
  // Get the new product entry row as a DOM element.
  var tableRow = document.querySelector('.product-inventory__new-product-entry');
  // Get the array of cells inside the product entry row.
  var tableCells = tableRow.querySelectorAll('td');

  // Serialize the data for the AJAX request.
  var data = '';
  for (var i = 0; i < tableCells.length; i++) {
    var input = tableCells[i].querySelector('input');
    data += input.name + '=' + input.value;
    if (i < tableCells.length) {
      data += '&';
    }
  };

  ajaxRequest('POST', 'http://wt.ops.few.vu.nl/api/9ca8e4fc', data, function(response, error) {
    if (error) {
      // If an error ocures send it to the console.
      console.error(error.code, error.message);
    } else if (response) {
      // If we get a resonse populate the product inventory.
      populateInventory();
    }
  });
};

function resetInventory() {
  ajaxRequest('GET', 'http://wt.ops.few.vu.nl/api/9ca8e4fc/reset', false, function(response, error) {
    if (error) {
      // If an error ocures send it to the console.
      console.error(error.code, error.message);
    } else if (response) {
      // If we get a resonse let the console know and re-populate the product inventory.
      // NOTE: Why is the key with a capital S?
      console.info(response.Success);
      populateInventory();
    }
  });
};

window.onload = function() {
  var apiKey = '9ca8e4fc';
  var resetButton = document.querySelector('.product-inventory__reset');
  var productInventoryForm = document.querySelector('#product_inventory');

  // Populate the table with product inventory from the API.
  populateInventory();

  // Listen for a click on the reset button and reset the product inventory.
  resetButton.addEventListener('click', function() {
    resetInventory();
  });

  // Listen for a form submet and add an item to the product inventory.
  productInventoryForm.addEventListener('submit', function(event) {
    event.preventDefault();
    addInventoryItem();
  });
};
