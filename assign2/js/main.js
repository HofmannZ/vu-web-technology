var apiKey = '9ca8e4fc';
var productInventoryList = document.querySelector('.product-inventory__list');
var resetButton = document.querySelector('.product-inventory__reset');

function ajaxRequest(method, url, callback) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
      callback(JSON.parse(this.responseText));
    } else if (this.readyState === 4) {
      // Some custom error handeling with callbacks, ES6 promises would be awesome here.
      callback(null, {
        code: this.status,
        message: 'An error has ocured.',
      });
    }
  };
  xhttp.open(method, url, true);
  xhttp.send();
};

function resetProductInventory(apiKey) {
  ajaxRequest('GET', 'http://wt.ops.few.vu.nl/api/' + apiKey + '/reset', function(response, error) {
    if (error) {
      console.error(error.code, error.message);
    } else if (response) {
      // Why is the key with a capital S?
      console.info(response.Success);
    }
  });
};

function fetchProductInventory(apiKey, callback) {
  ajaxRequest('GET', 'http://wt.ops.few.vu.nl/api/' + apiKey, function(response, error) {
    if (error) {
      console.error(error.code, error.message);
    } else if (response) {
      callback(response);
    }
  });
};

function renderInventoryItem(inventoryItem, productInventoryList) {
  var position = productInventoryList.querySelectorAll('tr').length - 1;
  var row = productInventoryList.insertRow(position);

  var name = row.insertCell(-1);
  var category = row.insertCell(-1);
  var amount = row.insertCell(-1);
  var location = row.insertCell(-1);
  var date = row.insertCell(-1);

  name.innerHTML = inventoryItem.name;
  category.innerHTML = inventoryItem.category;
  amount.innerHTML = inventoryItem.amount;
  location.innerHTML = inventoryItem.location;
  date.innerHTML = inventoryItem.date;
};

function renderProductInventory(apiKey, productInventoryList) {
  fetchProductInventory(apiKey, function(productInventory) {
    for (var i = 0; i < productInventory.length; i++) {
      renderInventoryItem(productInventory[i], productInventoryList);
    };
  });
};

renderProductInventory(apiKey, productInventoryList);

resetButton.addEventListener('click', function() {
  resetProductInventory(apiKey);
});
