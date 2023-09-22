// Stepper functionality from the provided link
const steps = document.querySelectorAll(".step");
const contents = document.querySelectorAll(".content");

steps.forEach((step, index) => {
    step.addEventListener("click", () => {
        steps.forEach((step) => step.classList.remove("active"));
        step.classList.add("active");
        
        contents.forEach((content) => content.classList.remove("active"));
        contents[index].classList.add("active");
    });
});

// Fire risk assessment dynamic scoring
document.querySelectorAll('.checkbox-container input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        let scoreChange = parseInt(this.getAttribute('data-score'));
        let overallScoreElem = document.getElementById('overallScore');
        let newScore = parseInt(overallScoreElem.innerText) + (this.checked ? scoreChange : -scoreChange);
        overallScoreElem.innerText = newScore;

        // Update the risk bar width and color based on the new score
        let riskBar = document.getElementById('riskBar');
        riskBar.style.width = (newScore / 100) * 100 + '%';
        riskBar.style.backgroundColor = newScore < 50 ? 'red' : (newScore < 75 ? 'yellow' : 'green');
    });
});

// document.querySelector('.btn').addEventListener('click', function() {
    // Some functionality
// });