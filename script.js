// 1. Select the elements
const rateInput = document.getElementById('rate');
const hoursInput = document.getElementById('hours');
const calcButton = document.getElementById('calculate-btn');
const resultDiv = document.getElementById('result');

// 2. Define the calculation function
function calculateTotal() {
    const rate = parseFloat(rateInput.value);
    const hours = parseFloat(hoursInput.value);

    if (isNaN(rate) || isNaN(hours)) {
        resultDiv.innerText = "Please enter valid numbers";
    } else {
        const total = rate * hours;
        resultDiv.innerText = "Total: $" + total.toFixed(2);
    }
}

// 3. Add the Event Listener
calcButton.addEventListener('click', calculateTotal);

// 4. Select the Clear button
const clearButton = document.getElementById('clear-btn');

// 5. Define the clear function
function clearForm() {
    rateInput.value = '';
    hoursInput.value = '';
    resultDiv.innerText = 'Total: $0';
}

// 6. Add the Event Listener for Clear
clearButton.addEventListener('click', clearForm);