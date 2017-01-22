function ajaxRequest(method, url, data, callback) {
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
  if (data) {
    xhttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhttp.send(data);
  } else {
    xhttp.send();
  }
};

function renderInventoryItem(inventoryItem) {
  var productInventoryList = document.querySelector('.product-inventory__list');
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

function renderInventory(productInventory) {
  for (var i = 0; i < productInventory.length; i++) {
    renderInventoryItem(productInventory[i]);
  };
};

function resetInventory() {
  ajaxRequest('GET', 'http://wt.ops.few.vu.nl/api/9ca8e4fc/reset', false, function(response, error) {
    if (error) {
      console.error(error.code, error.message);
    } else if (response) {
      // Why is the key with a capital S?
      console.info(response.Success);
    }
  });
};

function fetchInventory(callback) {
  ajaxRequest('GET', 'http://wt.ops.few.vu.nl/api/9ca8e4fc', false, function(response, error) {
    if (error) {
      console.error(error.code, error.message);
    } else if (response) {
      callback(response);
    }
  });
};

function addInventoryItem() {
  var tableRow = document.querySelector('.product-inventory__new-product-entry');
  var tableCells = tableRow.querySelectorAll('td');
  var data = {};

  for (var i = 0; i < tableCells.length; i++) {
    var input = tableCells[i].querySelector('input');
    data[input.name] = input.value;
  }

  ajaxRequest(
    'POST',
    'http://wt.ops.few.vu.nl/api/9ca8e4fc',
    JSON.stringify(data),
    function(response, error) {
      if (error) {
        console.error(error.code, error.message);
      } else if (response) {
        // Why is the key with a capital S?
        console.log(response);
      }
    }
  );
};

function initializeInventory() {
  fetchInventory(function(productInventory) {
    renderInventory(productInventory);
  });
};

window.onload = function() {
  var apiKey = '9ca8e4fc';
  var resetButton = document.querySelector('.product-inventory__reset');
  var productInventoryForm = document.querySelector('#product_inventory');

  initializeInventory();

  resetButton.addEventListener('click', function() {
    resetInventory();
  });

  productInventoryForm.addEventListener('submit', function(event) {
    event.preventDefault();
    addInventoryItem();
  });
}
