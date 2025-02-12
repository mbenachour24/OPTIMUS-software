<template>
    <div>
      <header>
        <h1>Optimus - About</h1>
      </header>
  
      <aside class="sidebar">
        <h3>Navigation</h3>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
        </ul>
        <h3>Systems</h3>
        <ul>
          <li><a href="/judicial">Judicial System</a></li>
          <li><a href="/political">Political System</a></li>
          <li><a href="/norms">View Norms</a></li>
          <li><a href="/cases">View Cases</a></li>
        </ul>
        <h3>Analytics</h3>
        <ul>
          <li class="has-submenu">
            <a href="/general_log">General Log</a>
            <ul class="submenu">
              <li><a href="/general_log#todays-activities">Today's Activities</a></li>
              <li><a href="/general_log#norm-updates">Norm Updates</a></li>
              <li><a href="/general_log#case-decisions">Case Decisions</a></li>
            </ul>
          </li>
          <li><a href="/statistics">Statistics Dashboard</a></li>
        </ul>
      </aside>
  
      <main class="main-content">
        <h2>About Optimus</h2>
  
        <section>
          <h3>Introduction</h3>
          <p>Optimus is a computational model designed to simulate and analyze the interaction between political and judicial systems. It transforms theoretical concepts of the Rule of Law into a dynamic, interactive software framework.</p>
        </section>
  
        <section>
          <h3>Systemic Modeling of the Rule of Law</h3>
          <p>Niklas Luhmann's theory is a way of understanding how society works by dividing it into different "systems". These systems are like groups or departments, and each has its own purpose and way of functioning. Examples include the judicial system, the political system, and the economic system.</p>
  
          <h4>Key Concepts of Luhmann's Theory:</h4>
          <ul>
            <li><strong>Functional Differentiation:</strong> Society is like a team, where each player has a specific role. For example:
              <ul>
                <li>The political system decides what's legal or illegal in general.</li>
                <li>The legal system judges cases based on what's legal.</li>
              </ul>
            </li>
            <li><strong>Autopoiesis:</strong> Each system operates independently with its own rules:
              <ul>
                <li>The political system creates norms.</li>
                <li>The judicial system creates judgments.</li>
              </ul>
            </li>
            <li><strong>Structural Coupling:</strong> Systems work together when needed (e.g., laws created by politics are used by judges, reviews made by judges can censor laws).</li>
            <li><strong>Society as an Iterative Process:</strong> Society ensures that systems interact over time, like a clock ticking. The temporal iterative process of society is what makes concepts like the Rule of Law exist.</li>
          </ul>
  
          <h4>3.1 First-Order Analysis: The Distinction between Judge and Norm</h4>
          <p>Rudimentarily and fundamentally, the judicial system can be reduced to two essential elements:</p>
          <ul>
            <li>The “subject” judge, responsible for basing their judgment on a norm.</li>
            <li>The “object” norm, which serves as a reference for the judge's decisions.</li>
          </ul>
          <embed src="static/images/Judge-law interaction.pdf" width="800px" height="600px" type="application/pdf">
          <figcaption>Illustration 1: Interaction Between the Norm and the Judge</figcaption>
  
          <h4>3.2 Second-Order Analysis: The Distinction between Legal and Political Systems</h4>
          <p>The four fundamental rules for second-order observations are:</p>
          <ul>
            <li>Functional Differentiation</li>
            <li>Autopoiesis</li>
            <li>Structural Coupling</li>
            <li>Society</li>
          </ul>
          <embed src="static/images/struc coup.pdf" width="800px" height="600px" type="application/pdf">
          <figcaption>Illustration 2: Autonomy and Structural Coupling of Legal and Political Systems</figcaption>
        </section>
  
        <section>
          <h3>Algorithmic Translation</h3>
          <p>The systemic principles are translated into Python classes, including:</p>
          <ul>
            <li><strong>PoliticalSystem:</strong> Simulates norm creation.</li>
            <li><strong>JudicialSystem:</strong> Processes cases based on norms.</li>
            <li><strong>Society:</strong> Orchestrates interactions between the two systems.</li>
          </ul>
          <embed src="static/images/whole.pdf" width="800px" height="600px" type="application/pdf">
          <figcaption>Illustration 3: Algorithmic Translation of Systemic Rules</figcaption>
        </section>
  
        <section>
          <h3>License & Contact</h3>
          <p>Optimus is released under the <strong>CC BY-NC 4.0</strong> license, meaning it is available for non-commercial use only.</p>
          <p>For inquiries, contact the project author at <a href="mailto:mbenachour24@gmail.com">mbenachour24@gmail.com</a>.</p>
        </section>
      </main>
  
      <footer>
        © 2025 Optimus Interface - Enhancing Rule of Law through Systems Interaction
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    name: 'AboutOptimus',
  };
  </script>
  
  <style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  :root {
    --primary: #2563eb;
    --sidebar-width: 280px;
    --header-height: 60px;
  }
  
  body {
    font-family: system-ui, -apple-system, sans-serif;
    background: #f9fafb;
  }
  
  header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: var(--header-height);
    background: white;
    padding: 0 1.5rem;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #e5e7eb;
    z-index: 20;
  }
  
  .sidebar {
    position: fixed;
    top: var(--header-height);
    left: 0;
    width: var(--sidebar-width);
    height: calc(100vh - var(--header-height));
    background: white;
    border-right: 1px solid #e5e7eb;
    padding: 1.5rem;
    overflow-y: auto;
  }
  
  .sidebar h3 {
    color: #6b7280;
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 1.5rem 0 0.75rem;
  }
  
  .sidebar h3:first-child {
    margin-top: 0;
  }
  
  .sidebar ul {
    list-style: none;
    margin-bottom: 1rem;
  }
  
  .sidebar li {
    margin: 0.5rem 0;
  }
  
  .sidebar a {
    color: #374151;
    text-decoration: none;
    display: block;
    padding: 0.5rem;
    border-radius: 0.375rem;
    transition: all 0.2s;
  }
  
  .sidebar a:hover {
    background: #f3f4f6;
    color: var(--primary);
  }
  
  .submenu {
    margin-left: 1rem;
    font-size: 0.875rem;
    display: none;
  }
  
  .has-submenu:hover .submenu {
    display: block;
  }
  
  .main-content {
    margin-left: var(--sidebar-width);
    margin-top: var(--header-height);
    padding: 2rem;
  }
  
  .main-content h2 {
    color: #111827;
  }
  
  .main-content section {
    margin-bottom: 2rem;
  }
  
  .main-content h3 {
    color: #111827;
    margin-bottom: 1rem;
  }
  
  .main-content p, .main-content ul {
    margin-bottom: 1rem;
  }
  
  .main-content embed {
    display: block;
    margin: 1rem 0;
  }
  
  .main-content figcaption {
    text-align: center;
    color: #6b7280;
    margin-top: 0.5rem;
  }
  
  footer {
    margin-left: var(--sidebar-width);
    padding: 1.5rem;
    text-align: center;
    color: #6b7280;
    border-top: 1px solid #e5e7eb;
  }
  
  @media (max-width: 1024px) {
    .sidebar {
      transform: translateX(-100%);
      transition: transform 0.3s;
    }
  
    .sidebar.active {
      transform: translateX(0);
    }
  
    .main-content, footer {
      margin-left: 0;
    }
  }
  </style>
  