const stepNext = document.querySelectorAll('.step-next');
const stepBack = document.querySelectorAll('.step-back');
const progress = document.querySelector('#progress');
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

const emailTemplateContainer = document.getElementById("template-container")
const emailTemplates = document.querySelectorAll(".email-template")

const emailFormContainer = document.getElementById("email-form-container")


const disapproveButtons = document.querySelectorAll(".disapprove-button")
const changeAudioButtons = document.querySelectorAll(".change-audio-button")
const showResultButtons = document.querySelectorAll(".show-result-button")
const detailsButtons = document.querySelectorAll(".details-button")
const campaignRows = document.querySelectorAll(".campaign-row")

let dataTable;

let pageLength = 100
const itemsPerPage = 100;
let currentPage = 1;


const fetchResult = async (base_url, campaign_id, query) => {
    const result = await fetch(`${base_url}/campaigns/${campaign_id}/paged_masked_calls?page=${currentPage}&per_page=${itemsPerPage}&search=${query}`, {
        method: "get",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    })
    return await result.json()

}


showResultButtons.forEach(button => {
    button.addEventListener("click", async (e) => {
            const campaign_id = e.currentTarget.getAttribute("data-ca")
            let searchValue = ""
            const base_url = document.getElementById("base-url").value
            const table = document.getElementById("show-result-table-body")
            const user = table.getAttribute("data-ca")
            const showResultPaginationBody = document.getElementById("result-pagination-body")
            const searchInput = document.getElementById("result-search")
            document.getElementById("show-result-label").innerHTML = `Show Result Campaign-${campaign_id}`
            showResultModal.show()
            try {
                const data = await fetchResult(base_url, campaign_id, searchValue)

                const paginationOptions = data["pagination"]
                showResultPaginationBody.innerHTML = ""
                for (let i = 1; i <= paginationOptions.total_pages; i++) {

                    showResultPaginationBody.innerHTML += `
                       <li class="page-item ">
                           <button class="page-link show-result-pagination-button page" id="page-${i}" data-page="${i}">${i}</button>
                       </li>
                    `
                }
                document.querySelector("#page-1").classList.add("active")

                if (!dataTable) {
                    dataTable = new DataTable('#show-result-table', {
                        data: data["calls"],
                        columns: [
                            {"data": "operation_id"},
                            {"data": "called_name"},
                            {"data": "called_address"},
                            {"data": "operation_phone_number"},
                            {"data": "called_email"},
                            {"data": "called_zip"},
                            {"data": "called_state"},
                        ],
                        paging: false,
                        lengthChange: false,
                        pageLength: pageLength,
                        searching: false,
                    });
                } else {
                    dataTable.clear().rows.add(data["calls"]).draw()
                }


                const paginationBehavior = () => {
                    const paginationButtons = document.querySelectorAll(".show-result-pagination-button")
                    paginationButtons.forEach(item => {
                        item.addEventListener("click", async (e) => {
                            currentPage = e.currentTarget.getAttribute("data-page")
                            const result = await fetchResult(base_url, campaign_id, searchValue)
                            dataTable.clear().rows.add(result["calls"]).draw()
                            document.querySelector(`.page.active`).classList.remove("active")
                            item.classList.add("active")
                        })
                    })

                }
                paginationBehavior()

                searchInput.addEventListener("input", async (e) => {
                    searchValue = e.target.value
                    const result = await fetchResult(base_url, campaign_id, searchValue)
                    dataTable.clear().rows.add(result["calls"]).draw()
                    const paginationOptions = result["pagination"]
                    showResultPaginationBody.innerHTML = ""
                    for (let i = 1; i <= paginationOptions.total_pages; i++) {
                        showResultPaginationBody.innerHTML += `
                       <li class="page-item ">
                           <button class="page-link show-result-pagination-button page" id="page-${i}" data-page="${i}">${i}</button>
                       </li>
                    `
                    }
                    document.querySelector("#page-1").classList.add("active")
                    paginationBehavior()
                })

                dataTable.on("click", "tr", async function () {
                    const rowData = dataTable.row(this).data()
                    if (rowData) {
                        const operationId = rowData.operation_id;
                        try {
                            const newResult = await fetch(`${base_url}/campaigns/unmasked?call_id=${operationId}&user_id=${user}&campaign_id=${campaign_id}`, {
                                method: "get",
                                headers: {
                                    "Content-Type": "application/json",
                                    "Accept": "application/json",
                                }

                            })
                            const newData = await newResult.json()
                            const rowIndex = dataTable.row(this).index()
                            if (newData.remaining_views && newData.remaining_views == 0) {
                                alert("you cant see anymore of unmasked data from this campaign")
                            } else {
                                dataTable.row(rowIndex).data(newData[0]).draw();
                            }
                        } catch (err) {
                            console.error(err)
                        }
                    }
                })
            } catch
                (e) {
                table.innerHTML = `
             <tr>
                 <td colspan="7" align="center">
                    <p class="text-danger fw-bold">
                        loading data failed <br/> please try later      
                    </p>
                 </td>
             </tr>
            `
            }
        }
    )
})


detailsButtons.forEach(button => {
    button.addEventListener("click", async (e) => {
        const campaign_id = e.currentTarget.getAttribute("data-ca")
        document.getElementById("details-modal-title").innerHTML = `Campaign-${campaign_id}`
        const result = await fetch(`/dashboard/admin/campaigns/list/?id=${campaign_id}`, {
            method: "get",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        })
        const data = await result.json()
        document.getElementById("details-modal-body").innerHTML =
            `
            <div class="card border-1 my-3">
                <div class="card-header">
                    SMS
                </div>
                <div class="card-body">
                    ${data[0]?.sms?.body}
                </div>
            </div>
            
            <div class="card border-1 my-3">
                <div class="card-header">
                    Email
                </div>
                <div class="card-body">
                <p>Subject: ${data[0]?.email?.subject}</p>
                    ${data[0]?.email?.body}
                </div>
            </div>
            
            <div class="card border-1 my-3">
                <div class="card-header">
                    Audio
                </div>
                <div class="card-body">
                    ${data[0]?.audio?.text}
                </div>
            </div>
            `
        detailsModal.show()
    })
})

disapproveButtons.forEach(button => {
    button.addEventListener("click", (e) => {
        const campaign_id = e.currentTarget.getAttribute("data-ca")
        document.getElementById("disapprove-modal-title").innerHTML = `Disapprove campaign-${campaign_id}`
        document.getElementById("disapprove-campaign-id").value = campaign_id
        disapproveModal.show()
    })
})

changeAudioButtons.forEach(button => {
    button.addEventListener("click", (e) => {
        const campaign_id = e.currentTarget.getAttribute("data-ca")
        document.getElementById("change-audio-modal-title").innerHTML = `Change audio campaign-${campaign_id}`
        document.getElementById("change-audio-campaign-id").value = campaign_id
        changeAudioModal.show()
    })

})


Array.from(stepBack).forEach((button, index) => {
    button.addEventListener('click', () => {
        let old_value = parseInt(progress.getAttribute("value"))
        progress.setAttribute('value', old_value - 25);
        const stepButton = document.getElementById(`step-button-${index + 1}`)
        stepButton.classList.remove("done")
    })
})


Array.from(stepNext).forEach((button, index) => {
    button.addEventListener('click', () => {
        let old_value = parseInt(progress.getAttribute("value"))
        progress.setAttribute('value', old_value + 25);
        const stepButton = document.getElementById(`step-button-${index + 1}`)
        stepButton.classList.add("done")
    })
})


function checkFormCompletion() {
    let currentStepForm = document.querySelector('.collapse.show');
    if (currentStepForm) {
        let requiredFields = currentStepForm.querySelectorAll('[required]');
        let isFormComplete = true;
        let counter
        if (requiredFields)
            requiredFields.forEach(function (field) {
                if (!field.value) {
                    isFormComplete = false;
                }
            });
        let button_one = currentStepForm.classList.contains("one")
        let button_two = currentStepForm.classList.contains("two")
        let button_three = currentStepForm.classList.contains("three")
        let button_forth = currentStepForm.classList.contains("forth")


        if (button_one)
            counter = "one"
        if (button_two)
            counter = "two"
        if (button_three)
            counter = "three"
        if (button_forth)
            counter = "forth"

        if (counter !== null || counter !== "undefined" || counter !== undefined) {
            let nextButton = document.querySelector(`.step-next.${counter}`);
            nextButton.disabled = !isFormComplete;
        }
    }

}

let formFields = document.querySelectorAll('input, select, textarea');
formFields.forEach(function (field) {
    field.addEventListener('input', checkFormCompletion);
});

let secondStep = document.getElementById('collapseTwo');
if (secondStep)
    secondStep.addEventListener('shown.bs.collapse', checkFormCompletion);


emailTemplates.forEach(item => {
    item.addEventListener("click", (e) => {
        const id = e.currentTarget.getAttribute("data-template")
        const previousActive = document.querySelector(".email-template.active")
        if (previousActive)
            previousActive.classList.remove("active")
        item.classList.add("active")
        document.getElementById("selected-template").value = id
        if (emailFormContainer.classList.contains("visually-hidden"))
            emailFormContainer.classList.remove("visually-hidden")
    })
})
