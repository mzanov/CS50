addEventListener("DOMContentLoaded", () => {
document.querySelectorAll('.redeem-form').forEach(form => {
    form.addEventListener('submit', function(event) {
        const rewardId = this.querySelector('.reward-id').value;
        const rewardName = this.parentNode.firstChild.textContent.trim();
        const pointsRequirement = this.parentNode.childNodes[2].textContent.split('-')[1].trim();
        
        if (!confirm(`Are you sure you want to redeem ${rewardName} for ${pointsRequirement} Points?`)) {
            event.preventDefault();
        }
    });
}); 
});