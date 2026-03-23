This HLD template is designed to be the "source of truth" for our modernization efforts. It bridges the gap between our current legacy state and our target architecture while aligning strictly with our [**Definition of Done (DoD)**](https://thoughtindustries.atlassian.net/wiki/spaces/ENGINEERIN/pages/753665/Definition+of+Done)—ensuring that development work is completed per scope and all subtasks are resolved before we even think about a PR.

# ---

**High-Level Design (HLD): \[Feature Name\]**

**Author:** \[Lead Engineer Name\]

**Date:** YYYY-MM-DD

**Status:** \[Draft / Under Review / Approved\]

**Jira Epic:** \[Link to Jira\]

## ---

**1\. Executive Summary**

* **Goal:** What specific problem are we solving?  
* **Business Value:** How does this impact the customer or our bottom line?  
* **Technical Impact:** Which systems are touched and what is the "blast radius"?

**Architect’s Guidance:** *If I can't understand the value in three sentences, the scope is too fuzzy.* 

## ---

**2\. The 'Strangler' Migration Plan**

* **Interoperability:** How does the new NestJS/React code communicate with legacy Node/Ember?  
* **Routing:** How is traffic sliced at the API Gateway or CloudFront level?  
* **State Management:** Are we sharing a database? If so, how are we preventing the legacy app from corrupting new schemas?

**Architect’s Guidance:** *Modernization is surgery. Tell me exactly how we’re keeping the patient (the legacy app) alive while we're replacing the heart.*

## ---

**3\. Proposed Architecture**

* **NestJS (Backend):** Module breakdown, service dependencies, and DTO definitions.  
* **React (Frontend):** Component hierarchy, state management, and styling approach (based on Design library).  
* **Integration:** Describe the contract between the new FE and BE.

**Architect’s Guidance:** *I'm looking for modularity. If your NestJS modules are tightly coupled, we're just building a "distributed monolith." Keep it clean.*

## ---

**4\. Options Analysis**

### **Option A (Proposed)**

* **Pros:** Why this is the winner.  
* **Cons:** What are we giving up?  
* **Technical Risks:** What could go wrong during implementation?

### **Option B (Alternative)**

* **Pros/Cons:** Why was this considered?  
* **Rejection Reason:** Why did we decide against it?

### **Option C (The 'Status Quo')**

* **Why we can't stay here:** Document the specific technical debt or performance bottlenecks of the legacy implementation.

**Architect’s Guidance:** *Confirmation bias is a project killer. If you can't give me a valid Option B, you haven't thought deeply enough about the constraints.*

Summary

| Options | Pros | Cons |
| :---- | :---- | :---- |
|  |  |  |
|  |  |  |

**NOTE:** There can be as many options analysis that the HLD requires to cover in order to address the scope of the HLD.

## ---

**5\. Engineering Recommendation**

* **Statement of Intent:** A formal justification from the lead engineer. Why is Option A the most scalable and maintainable path?

**Architect’s Guidance:** *This is your professional signature. Own the trade-offs and justify the "Why" relative to our 2-year growth plan.*

## ---

**6\. Anti-Regression & QA Strategy**

* **Test Plan:**  
  * **Unit (Jest):** Coverage targets for logic-heavy services.  
  * **Integration:** How we’re testing NestJS controllers and DB interactions.  
  * **E2E (Playwright):** Critical user paths that must not break.  
* **Parity Verification:** Specific checklist to ensure the React UI matches (or intentionally improves) Ember functionality.  
* **Observability:** Which CloudWatch metrics or custom alerts will trigger if a regression hits production?

**Architect’s Guidance:** *Per our DoD, "Feature passes end to end regression" is non-negotiable. Don't just tell me you'll test it—tell me how the machine will prove it's not broken.*

## ---

**7\. Data & Infrastructure**

* **Schema Changes:** New tables, altered columns, or migrations.  
* **AWS Resources:** K8s pod specs, RDS instance sizing, or S3 bucket requirements.  
* **Cost Estimate:** Expected monthly AWS spend at 10x current scale.

**Architect’s Guidance:** *Storage is cheap, but compute and "oops" architectural choices are expensive. Design for the scale we want, not the scale we have.*

## ---

**8\. Security & Compliance**

* **AuthN/AuthZ:** How are we handling permissions in the new stack?  
* **Data Privacy:** Impact on GDPR/SOC2.  
* **Encryption:** Verification of data at rest and in transit.

**Architect’s Guidance:** *Security isn't a "last step." If you're touching user data, I expect to see the isolation boundaries clearly defined here.*

