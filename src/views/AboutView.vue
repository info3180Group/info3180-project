<template>
  <div class="about container">
    <h2>About JamDate</h2>
    <p>Welcome to JamDate, your ultimate date-matching application designed to help you find meaningful connections. 
      Whether you're looking for friendship, romance, or just someone to share your interests with, 
      JamDate is here to make your search easier and more enjoyable.</p>
    
    <h2>What We Offer</h2>
    <ul>
      <li><strong>Profile Creation:</strong> Create a detailed profile about yourself, highlighting your interests, hobbies, and what you're looking for in a match.</li>
      <li><strong>Advanced Matching:</strong> Search for potential matches based on various levels of compatibility with your profile. Our sophisticated algorithms ensure you find the best possible matches.</li>
      <li><strong>Detailed Insights:</strong> Get more information on users who match your profile. Learn about their interests, hobbies, and what makes them unique.</li>
      <li><strong>Favorites:</strong> Add a tick to your favorite profiles to keep track of users you are most interested in.</li>
      <li><strong>Reports and Analytics:</strong> View insightful reports on the collection of users. Discover who is the most favorite among users and see detailed statistics on who matches your profile.</li>
    </ul>

    <h2>Our Mission</h2>
    <p>At JamDate, our mission is to create a platform where connections are made effortlessly. 
      We believe in the power of technology to bring people together and foster meaningful relationships. 
      Join us and start your journey to finding your perfect match today!</p>
  </div>
</template>


<style scoped>
.about.container {
  max-width: 960px;
  margin: 60px auto;
  padding: 40px;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.7;
  color: #333;
}

.about h2 {
  color: #007BFF;
  margin-top: 30px;
  font-size: 26px;
}

.about p {
  font-size: 16px;
  margin-bottom: 20px;
}

.about ul {
  list-style-type: disc;
  padding-left: 20px;
  margin-bottom: 30px;
}

.about li {
  margin-bottom: 15px;
  font-size: 16px;
}

.about li strong {
  color: #343a40;
}

@media (max-width: 768px) {
  .about.container {
    padding: 20px;
  }

  .about h2 {
    font-size: 22px;
  }

  .about p,
  .about li {
    font-size: 15px;
  }
}
</style>

