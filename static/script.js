function validateForm(event) {
    
    const monthlyCharges = document.getElementById('query2').value;
    const totalCharges = document.getElementById('query3').value;
    const tenure = document.getElementById('query19').value;

 
    if (!monthlyCharges || !totalCharges || !tenure) {
        event.preventDefault(); 
        alert('Please fill in all required fields: Monthly Charges, Total Charges, and Tenure.');
    }
}
function clearOutput() {
    document.getElementById('output1').value = '';
    document.getElementById('output2').value = '';
}
