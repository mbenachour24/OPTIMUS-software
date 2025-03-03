<template>
  <div>
    <!-- Header -->
    <header>
      <h1>Optimus - Systemic Modelling</h1>
    </header>

    <!-- Sidebar -->
    <aside class="sidebar">
      <h3>Navigation</h3>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about" class="active-link">About</a></li>
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
        <li><a href="/statistics">Statistics Dashboard</a></li>
      </ul>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <h1>1.1. Systemic Modelling of the Rule of Law</h1>
      <p>
        The systemic theory we were discussing is modellable graphically and algorithmically. To model the Rule of Law using a systemic method, we must consider two levels of observation:
      </p>
      <ul>
        <li>First, the <strong>first-order observation</strong>: From an objective point of view, the distinction between the judge and the norm (1.1.1).</li>
        <li>Then, the <strong>second-order observation</strong>: From a systemic point of view, the distinction between the judicial system and the political system (1.1.2).</li>
      </ul>

      <h2>1.1.1. First-Order Analysis: The Distinction between Judge and Norm</h2>
      <div>
        <img :src="judgeLawImage" alt="Interaction Between the Norm and the Judge" />
        <p>Illustration 1: Interaction Between the Norm and the Judge</p>
      </div>
      <p>
        Rudimentarily and fundamentally, the judicial system can be reduced to two essential elements:
      </p>
      <ul>
        <li>On one hand, <strong>the 'subject' judge</strong>, the human element, the 'human resource' of the judicial system. The judge is responsible for basing their judgement on a norm.</li>
        <li>On the other hand, <strong>the 'object' norm</strong> (constitutional norm, positive law, regulation, and, generally, any valid rule). The norm serves as a reference object for the judge, providing a foundation for the judgement to be made.</li>
      </ul>
      <p>
        <strong>the judge is structurally linked to the norm through the reference operation. The proposition is equally valid in both directions: the norm is structurally linked to the judge through the reference operation. There is no norm without a judge (voluntarism), and no judge without a norm (normativism).</strong> The dialectic between rationalism and voluntarism on which 20th century legal theory was founded does not concern systems theory. There is a fundamental relationship between judges (voluntarist element) and norms (rational element). The interpretative activity of judges plays a central role in the application of norms, and the positive existence of norms grounds the function of the judge.
      </p>

      <h2>1.1.2. Second-Order Analysis: The Distinction between the Legal System and the Political System</h2>
      <div>
        <img :src="structuralCouplingImage" alt="Autonomy and Structural Coupling of Legal and Political Systems" />
        <p>Illustration 2: Autonomy and Structural Coupling of Legal and Political Systems</p>
      </div>
      <ul>
        <li> <strong>The political system</strong>: The political system is the generator of norms through its legislative and policy-making processes. The system operates autonomously, following its own logic (government/opposition) to produce the norms.</li>
        <li> <strong>The judicial system</strong>: the judicial system is responsible for case processing: creating judgements in which it will be applying and interpreting the norms produced by the political system. This system operates autonomously, following its own logic (legal/illegal) while processing cases by producing judgements.</li>
        <li> <strong>Their structural coupling</strong>: The reform arrow represents the binding influence of political reforms on judicial courts. In the structural coupling between the political and judicial systems, political reforms, such as the enactment of new laws or amendments to existing ones, create a framework that judicial courts must adhere to when interpreting and applying the law in judgements. This demonstrates how political decisions, once formalised as norms, shape the parameters within which judicial decisions are made. The review arrow, going from the political system to the judicial system, reflects the role of judicial review in assessing and validating political outputs, such as laws and regulations. This ensures that political decisions align with constitutional and legal frameworks. For example, court rulings can identify gaps, ambiguities, or constitutional issues in legislation, prompting the political system to revise or reform existing norms.</li>
        <li> <strong>Society</strong>: Encircling the entire diagram, society serves as the temporal iteration within which these systems interact. It acts as the source of social demands to produce norms and judgements: every iteration cases are brought before the courts, while the norms are the translation of political will demanded by the citizen political needs of society and articulated through legislative or regulatory processes. The circular representation emphasises the recursive and reciprocal nature of these processes. The functioning of society lies in its temporal recursive element, that serves as the condition for the interaction between the distinct processes of judicial and political systems: everyday, the court must process new cases while parliaments legislate on the pressing matters of daily governance.</li>
      </ul>
      <p>
        It is important to note that the structural coupling between the judicial system and the political system is not automatic; <strong>it results from the fundamental principle of the Rule of Law</strong>, and its establishment can only be achieved through constitutional means. <strong>The political system must be constitutionally authorised to produce norms, while the judicial system, also constitutionally mandated, has the mission of rendering judgements by referring to the existing political norms</strong>.
      </p>

      <h2>1.1.3. Fundamental Rules of the Rule of Law</h2>
      <p>
        Four fundamental rules for algorithmic modelling of the Rule of Law are directly deduced from the four elements of the second order distinction: functional differentiation, autopoiesis, structural coupling, and the functioning of society.
      </p>
      <ol>
        <li><strong>Rule of legality (differentiation & autopoiesis of the political system)</strong>: Every political decision must be considered a norm and be applicable within society.</li>
        <li><strong>Rule of interpretation (differentiation & autopoiesis of the judicial system)</strong>: Courts are required to produce judgements. Norms must be interpreted by the courts based on specific cases.</li>
        <li><strong>Rule of Checks and Balances (structural coupling)</strong>: Judicial decisions can influence future political decisions, and political decisions can influence future judicial decisions.</li>
        <li><strong>Rule of temporal recursion (functioning of society)</strong>: For the system to be 'alive', the operation of the judge referencing the norm must be iterated in time. Social temporality paces the operations of the judicial system. Without the judge's active reference to the norm, the norm cannot be applied in society. The recursive functioning of society (typically, the flow of days, the work calendar) must take place for the Rule of Law to exist. This is commonly met in legal notions such as prescription, reasonable time, various procedural timelines, contractual durations, penalties, etc. In politics, it is operationalised through electoral calendars, terms of office, constitutionally prescribed deadlines, etc. Simply put, the court must open its doors in the morning and accept cases.</li>
      </ol>

      <h1>1.2. Algorithmic Translation of the Specific Systemic Rules Applicable to the Rule of Law</h1>
      <p>
        The four concepts to define and convert into code are: functional differentiation, autopoiesis, structural coupling, and society.
      </p>

      <h2>1.2.1. Functional Differentiation</h2>
      <p>
        Functional differentiation is the process by which social systems specialise and distinguish themselves according to their specific roles in society. In the context of the Rule of Law, this means that the judicial system and the political system have distinct, yet interdependent functions: the political system fulfils a decision-making function (represented by the PoliticalSystem class and the make_decision method), while the judicial system is dedicated to producing judgements (represented by the JudicialSystem class and the produce_cases method).
      </p>
      <div>
        <img :src="functionalDifferentiationImage" alt="Functional Differentiation" />
        <p>Illustration 3: The judicial system and the political system as two differentiated systems.</p>
      </div>
      <pre><code>
class PoliticalSystem:
    def __init__(self):
        self.norm_counter = 0
        self.norms = []
    def make_decision(self):
        """Simulates the creation of a norm by the political system."""
        self.norm_counter += 1
        norm = f"Norm {self.norm_counter}"
        self.norms.append(norm)
        print(f"Political System: Created {norm}")

class JudicialSystem:
    def __init__(self):
        self.case_counter = 0
        self.cases = []

    def produce_cases(self, norms):
        """Simulates the creation of cases based on norms provided by the political system."""
        for norm in norms:
            self.case_counter += 1
            case = f"Case {self.case_counter} based on {norm}"
            self.cases.append(case)
            print(f"Judicial System: Processed {case}")
      </code></pre>

      <h2>1.2.2. Autopoiesis</h2>
      <p>
        Autopoiesis, in the context of legal and political systems, describes how these systems generate and maintain themselves. The political system produces norms, while the judicial system generates judgements, including a reference to the norms.
      </p>
      <div>
        <img :src="autopoiesisImage" alt="Autopoiesis" />
        <p>Illustration 4: The two functionally differentiated systems produce operational units by which they reproduce their systemic unity.</p>
      </div>
      <pre><code>
class Norm:
    def __init__(self, norm_id, text, valid, complexity):
        self.id = norm_id
        self.text = text
        self.valid = valid
        self.complexity = complexity

class Case:
    def __init__(self, case_id, text, norm_id, constitutional, complexity):
        self.id = case_id
        self.text = text
        self.norm_id = norm_id
        self.constitutional = constitutional
        self.complexity = complexity
      </code></pre>

      <h2>1.2.3. Structural Coupling</h2>
      <p>
        Structural coupling refers to how two distinct systems, although operationally closed, can interact and influence each other's internal structures. For example, political decisions that produce norms must be interpreted and applied by the judicial system. Conversely, judicial decisions can impact future political decisions.
      </p>
      <div>
        <img :src="structuralCouplingImage" alt="Autonomy and Structural Coupling of Legal and Political Systems" />
        <p>Illustration 5: The two functionally differentiated systems are structurally coupled.</p>
      </div>
      <pre><code>
class JudicialSystem:
    def check_constitutionality(self, norm):
        if not norm.valid:
            norm.invalidate()

    def produce_cases(self):
        case = Case(case_id=1, text="Example Case", norm_id=norm.id, constitutional=True, complexity=5)

class PoliticalSystem:
    def __init__(self):
        self.norm_pool = []
        self.norm_counter = 0
        self.judicial_system = None

    def make_decision(self):
        new_norms = self.produce_norms_decision()
        for norm in new_norms:
            self.norm_pool.append(norm)
            norm.log_event("Created by political decision")
        return new_norms

    def produce_norms_decision(self):
        norm_id = self.norm_counter
        new_Law = Law(norm_id=norm_id, text=f'Law {norm_id}', valid=True, complexity=random.randint(COMPLEXITY_MIN, COMPLEXITY_MAX))
        self.norm_counter += 1
        return [new_Law]

    def reform_norm(self, norm_id):
        for norm in self.norm_pool:
            if norm.id == norm_id:
                norm.update_complexity(random.randint(-2, 2))
                norm.validate()
                norm.log_event("Reformed by political decision")
      </code></pre>

      <h2>1.2.4. Society</h2>
      <p>
        Society is the environment in which the political and judicial systems operate and interact. Its recursive process creates the necessary conditions for the existence and functioning of its subsystems by formulating expectations and exerting pressures that influence political and legal decisions.
      </p>
      <div>
        <img :src="societyImage" alt="Society" />
        <p>Illustration 6: The recursive functioning of society is a necessary condition for the functioning of both systems and their coupling.</p>
      </div>
      <pre><code>
class Society:
    def __init__(self):
        self.political_system = PoliticalSystem()
        self.judicial_system = JudicialSystem()
        self.iteration = 0

    async def simulate(self):
        while self.iteration < SIMULATION_DAYS:
            self.iteration += 1
            logging.info(f"\n\n---- DAY {self.iteration} ---\n")
            event = random.choice(["Economic Crisis", "Elections", "Natural Disaster"])
            logging.info(f"Political System: Random event occurred: {event}")
            await asyncio.sleep(0.1)
        logging.info("Simulation completed.")

async def main():
    society = Society()
    await society.simulate()

asyncio.run(main())
      </code></pre>
    </main>

    <!-- Footer -->
    <footer>
      © 2024 Optimus Interface - Enhancing Rule of Law through Systems Interaction
    </footer>
  </div>
</template>

<script>
import judgeLawImage from "@/assets/images/judge-law-interaction.jpg";
import structuralCouplingImage from "@/assets/images/structuralcoupling.jpg";
import functionalDifferentiationImage from "@/assets/images/functionaldifferentiation.jpg";
import autopoiesisImage from "@/assets/images/autopoiesis.jpg";
import societyImage from "@/assets/images/society.jpg";

export default {
  name: "SystemicModelling",
  data() {
    return {
      judgeLawImage,
      structuralCouplingImage,
      functionalDifferentiationImage,
      autopoiesisImage,
      societyImage,
    };
  },
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
  --font-family: 'Helvetica Neue', Arial, sans-serif;
}

body {
  font-family: var(--font-family);
  background: #f9fafb;
  color: #333;
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
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

header h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary);
}

.sidebar {
  position: fixed;
  top: var(--header-height);
  left: 0;
  width: var(--sidebar-width) !important;
  height: calc(100vh - var(--header-height)) !important;
  background: white;
  border-right: 1px solid #e5e7eb;
  padding: 1.5rem;
  overflow-y: auto;
  transition: transform 0.3s ease;
}

.sidebar h3 {
  color: #6b7280;
  font-size: 1rem;
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
  padding: 0.75rem 1rem;
  border-radius: 0.375rem;
  transition: all 0.2s ease;
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
  margin-left: var(--sidebar-width) !important;
  width: calc(100vw - var(--sidebar-width)) !important;
  min-height: 100vh;
  margin-top: var(--header-height);
  padding: 2rem;
  transition: margin-left 0.3s ease;
}

.main-content h1 {
  color: #111827;
  font-size: 2.25rem;
  margin-bottom: 1.5rem;
  margin-top: 2rem;
}

.main-content h2 {
  color: #111827;
  font-size: 1.75rem;
  margin-bottom: 1rem;
  margin-top: 1.5rem;
}

.main-content section {
  margin-bottom: 2rem;
}

.main-content h3 {
  color: #111827;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.main-content p, .main-content ul, .main-content ol {
  margin-bottom: 1rem;
  font-size: 1rem;
  line-height: 1;
}

.main-content ul, .main-content ol {
  padding-left: 2rem;
}

.main-content li {
  margin-bottom: 0.5rem;
}

.main-content embed {
  display: block;
  margin: 1rem 0;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
}

.main-content figcaption {
  text-align: center;
  color: #6b7280;
  margin-top: 0.5rem;
  font-size: 0.875rem;
}

/* Image styling */
.main-content img {
  max-width: 600px; /* Limits image width */
  width: 100%; /* Makes images responsive */
  height: auto; /* Maintains aspect ratio */
  display: block;
  margin: 1.5rem auto;
  border-radius: 0.375rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  object-fit: contain; /* Prevents distortion */
}

.main-content div {
  margin-bottom: 2rem;
}

/* Caption styling */
.main-content div > p:last-child {
  color: #111111;
  margin-top: 0.5rem;
  font-size: 1rem;
}

/* Code block styling */
.main-content pre {
  background-color: #f8f9fa;
  border-radius: 0.375rem;
  padding: 1rem;
  margin-bottom: 1.5rem;
  overflow-x: auto;
  border: 1px solid #e5e7eb;
}

.main-content code {
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  line-height: 1.5;
  color: #374151;
}

footer {
  margin-left: var(--sidebar-width);
  padding: 1.5rem;
  text-align: center;
  color: #6b7280;
  border-top: 1px solid #e5e7eb;
  background: white;
  transition: margin-left 0.3s ease;
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }

  .sidebar.active {
    transform: translateX(0);
  }

  .main-content, footer {
    margin-left: 0;
    width: 100% !important;
  }
  
  .main-content img {
    width: 100% !important;
    height: auto;
  }
}

/* Improved responsive styles for smaller screens */
@media (max-width: 768px) {
  .main-content {
    padding: 1.5rem;
  }
  
  .main-content h1 {
    font-size: 2rem;
  }
  
  .main-content h2 {
    font-size: 1.5rem;
  }
}
</style>
