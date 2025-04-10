document.addEventListener("DOMContentLoaded", () => {
    const INDUSTRY_LIST = [];
    const QUESTION_LIST = [];
    const businessSteps = []
    const audienceSteps = [
        {
            label: "What is the gender of your target audience?",
            input: `<select name="gender" class="form-select" required>
            <option value="">Select Gender</option>
            <option value="all">All Genders</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
        </select>`,
            name: "gender",
            help_text: "Choose the gender that your products or services are most aimed at. Select 'All Genders' if your business targets everyone."
        },
        {
            label: "What is the age range of your audience?",
            input: `<select name="age_range" class="form-select" required>
            <option value="">Select Age Range</option>
            <option value="1-6">1–6 years old</option>
            <option value="7-12">7–12 years old</option>
            <option value="13-19">13–19 years old</option>
            <option value="20-60">20–60 years old</option>
            <option value="60+">60+ years old</option>
        </select>`,
            name: "age_range",
            help_text: "Select the primary age group that your business focuses on."
        },
        {
            label: "What are your audience's main interests?",
            input: `<textarea name="interests" class="form-control" placeholder="e.g., technology, fashion, fitness, travel" required></textarea>`,
            name: "interests",
            help_text: "List the common interests of your target audience. This helps us understand what engages them. (Optional)"
        },
        {
            label: "What is the focus of your audience?",
            input: `<textarea name="focus" class="form-control" placeholder="e.g., urban professionals, eco-conscious families, adventure seekers" required></textarea>`,
            name: "focus",
            help_text: "Describe your audience focus — this could be their lifestyle, location, profession, or shared goals. (Optional)"
        },
    ];

    const csrfToken = document.body.getAttribute("data-csrf")
    const formData = {};
    let step = 0;

    const startButton = document.getElementById("start-questionnaire");
    const cardHeader = document.getElementById("card-header");
    const cardBody = document.getElementById("card-body");

    const getData = async (url) => {
        const response = await fetch(url);
        if (!response.ok) {
            console.error("Failed to fetch data:", response.statusText);
            return [];
        }
        return await response.json();
    };

    const renderFormFlow = (title, steps, dataKey, onComplete) => {
        let innerStep = 0;
        const collectedData = {};

        const renderInnerStep = () => {
            const current = steps[innerStep];
            cardHeader.innerHTML = `<h3 class="text-center">${title}</h3>`;
            cardBody.innerHTML = `
            <form id="multi-step-form">
                <div class="mb-3">
                    <label>${current.label}</label>
                    ${current.input}
                    <div class="form-text">${current.help_text}</div>
                </div>
                <button type="submit" class="btn btn-primary">
                    ${innerStep < steps.length - 1 ? "Next Question" : "Finish"}
                </button>
            </form>
        `;

            document.getElementById("multi-step-form").addEventListener("submit", (e) => {
                e.preventDefault();
                const form = e.target;
                const formField = form[current.name];
                collectedData[current.name] = formField ? formField.value : "";

                if (innerStep < steps.length - 1) {
                    innerStep++;
                    renderInnerStep();
                } else {
                    formData[dataKey] = collectedData;
                    onComplete(); // Next global step
                }
            });
        };

        renderInnerStep();
    };

    const renderStep = async () => {
        switch (step) {
            case 1:
                renderFormFlow(
                    'Business <strong class="text-primary">Information</strong>',
                    businessSteps,
                    'business',
                    () => {
                        step++;
                        renderStep();
                    }
                );
                break;
            case 2:
                renderFormFlow(
                    'Tell us About Your <strong class="text-primary">Audience</strong>',
                    audienceSteps,
                    'audience',
                    () => {
                        step++;
                        renderStep();
                    }
                );
                break;
            case 3:
                const selectedIndustry = formData?.business?.industry || 1;
                const questions = await getData(`/api/industry/questions/?industry=${selectedIndustry}`);

                const formattedQuestions = questions.map(question => {
                    let inputField = '';
                    switch (question.answer_type) {
                        case 'text':
                            inputField = `<input type="text" name="question_${question.id}" class="form-control" placeholder="${question.name}" required>`;
                            break;
                        case 'textarea':
                            inputField = `<textarea name="question_${question.id}" class="form-control" placeholder="${question.name}" required></textarea>`;
                            break;
                        // Add other types like 'select', 'checkbox', etc., as needed
                        default:
                            inputField = `<input type="text" name="question_${question.id}" class="form-control" placeholder="${question.name}" required>`;
                            break;
                    }

                    return {
                        label: question.name,
                        input: inputField,
                        name: `question_${question.id}`,
                        help_text: question.optional ? "This question is optional." : "This question is required."
                    };
                });

                QUESTION_LIST.push(...formattedQuestions);

                renderFormFlow(
                    'Now Here are some questions about your business industry.',
                    formattedQuestions,
                    "questions",
                    () => {
                        step++;
                        renderStep();
                    }
                );
                break;

            case 4:
                renderFinish();
                break;
            default:
                console.warn("Unknown step");
        }
    };


    const renderFinish = () => {
        cardHeader.innerHTML = `<h3 class="text-center">You are all set.</h3>`;
        cardBody.innerHTML = `
            <p class="text-center">thank you for finishing all the questions, click on button bellow to finalize everything.</p>
            <div class="text-center">
                <button class="btn btn-primary" id="submit-all">Finalize</button>
            </div>
        `;

        document.getElementById("submit-all")
            .addEventListener("click", async () => {
                try {
                    const prepData = JSON.stringify(formData)
                    const request = await fetch("/api/user/business/profile/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "X-CSRFToken": csrfToken,
                        },
                        body: prepData
                    })

                    if (request.ok) {
                        location.href = "/dashboard/"
                    } else {
                        console.log(await request.json())
                        alert("Something did go wrng, please try again or refresh the page")
                    }

                } catch (error) {
                    console.error("Submission failed:", error);
                    alert("Submission failed.");
                }
            });
    };

    startButton.addEventListener("click", async () => {
        const industries = await getData("/api/industry/");
        INDUSTRY_LIST.push(...industries);
        businessSteps.push(...[
            {
                label: "What is the name of your business?",
                input: `<input type="text" name="business_name" class="form-control" placeholder="e.g., Brew & Bean Café or Skyline Tech Solutions" required>`,
                name: "business_name",
                help_text: "Enter the official name of your business."
            },
            {
                label: "Which industry does your business belong to?",
                input: `<select name="industry" class="form-select" required>
            <option value="">Select Industry</option>
            ${INDUSTRY_LIST.map(ind => `<option value="${ind.id}">${ind.name}</option>`).join('')}
        </select>`,
                name: "industry",
                help_text: "Select the industry category that best represents your products or services."
            },
            {
                label: "Where is your business located?",
                input: `<input type="text" name="location" class="form-control" placeholder="e.g., New York City, USA or online only" required>`,
                name: "location",
                help_text: "Provide the main location of your business, or specify if it operates online."
            },
            {
                label: "Do you have a website?",
                input: `<input type="url" name="website" class="form-control" placeholder="https://yourwebsite.com">`,
                name: "website",
                help_text: "Enter your website URL to help customers find you online. (Optional)"
            },
            {
                label: "What are your operating hours?",
                input: `<input type="text" name="work_hours" class="form-control" placeholder="e.g., Mon–Fri, 9 AM – 5 PM" required>`,
                name: "work_hours",
                help_text: "Let us know when you're open for business."
            },
            {
                label: "How would you describe your brand tone?",
                input: `<input type="text" name="brand_tone" class="form-control" placeholder="e.g., Friendly, Professional, Playful">`,
                name: "brand_tone",
                help_text: "Describe the personality and style of your brand communication. (Optional)"
            },
            {
                label: "What are some keywords that describe your brand?",
                input: `<textarea name="brand_keywords" placeholder="e.g., organic, innovative, community-focused" class="form-control"></textarea>`,
                name: "brand_keywords",
                help_text: "List words or short phrases that represent your brand's essence. (Optional)"
            },
        ])
        step = 1;
        renderStep();
    });
});
