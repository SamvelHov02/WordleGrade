// User should be able to go back to the home page
const homeElement = document.getElementById('home');
homeElement.addEventListener("click", () => window.location.href = "choose_metric.html");

document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem('token');

    const res = await fetch('http://localhost:8000/api/profile', {
        headers : {"Authorization" : `Bearer ${token}`}
    });

    const data = await res.json();
    const quantityArray = [data['games_played'], data['win_rate'], data['current_streak'], data['best_streak']];
    console.log(data);
    
    // add the General Stat DOM nodes
    const generalStats = document.querySelectorAll('.stat-quantity');

    for (let i = 0; i < generalStats.length; i++){
        generalStats[i].textContent = quantityArray[i];
    }

    // Add the Grade Distribution
    const grades = data['grade_dist'];
    const all_grades = Object.values(grades);
    const total_grades = all_grades.reduce((acc, n) => acc + n, 0);
    const gradeRows = document.querySelectorAll('.grade-row');
    gradeRows.forEach((el) => {
        const key = el.id.slice(6);
        const count = grades[key];
        const barElement = el.querySelector('.grade-bar');
        const countElement = el.querySelector('.grade-count');
        
        countElement.textContent = count
        countElement.style.width = total_grades > 0 ? `${(count / total_grades) * 100}%` : "n/a";
    });

    // Add the recent games
    const recentGames = data['last_five_games'];
    const recentGamesElements = document.querySelectorAll('.recent-game');
    recentGamesElements.forEach((el, i) => {
        const gradeElement = el.querySelector('.recent-game-grade');
        const guessesElement = el.querySelector('.recent-game-guesses');
        console.log("Gets here");
        const grade = recentGames[i] ? recentGames[i].grade : "n/a";
        const guesses = recentGames[i] ? `${recentGames[i]['total_guesses']}/6`: "n/a";

        gradeElement.textContent = grade;
        guessesElement.textContent = guesses;
    });
});