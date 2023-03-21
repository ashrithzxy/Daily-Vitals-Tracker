let sampleForm = document.getElementById("vitals");

//Define the event handler for the form when it's submitted
sampleForm.addEventListener("submit", async (e) => {
    /**
     * Prevent the default browser behaviour of submitting
     * the form so that you can handle this instead.
     */
    e.preventDefault();
  
    /**
     * Get the element attached to the event handler.
     */
    let form = e.currentTarget;
  
    /**
     * Take the URL from the form's `action` attribute.
     */
    let url = form.action;
    // console.log("URL from form action is: ",url);
    try {
      /**
       * Takes all the form fields and make the field values
       * available through a `FormData` instance.
       */
      let formData = new FormData(form);
      // console.log("formData is: ",formData);
      // console.log("formData type is: ",typeof(formData));
  
      /**
       * The `postFormFieldsAsJson()` function in the next step.
       */
      let responseData = await postFormFieldsAsJson({ url, formData });
  
      //Destructure the response data
      let { serverDataResponse } = responseData;
  
      //Display the response data in the console (for debugging)
      console.log(serverDataResponse);
    } catch (error) {
      //If an error occurs display it in the console (for debugging)
      console.error(error);
    }
  });
  
  /**
   * Helper function to POST data as JSON with Fetch.
   */
  async function postFormFieldsAsJson({ url, formData }) {
    //Create an object from the form data entries
    let formDataObject = Object.fromEntries(formData.entries());
    // console.log("POST data is: ",formDataObject);
    // console.log("formDataObject type: ",typeof(formDataObject));
    // Format the plain form data as JSON
    let returnData = {
      "bloodPressure":[
      [
        formDataObject['systolic-reading-1'],
        formDataObject['diastolic-reading-1'],
        formDataObject['pulse-reading-1']
      ],
      [
        formDataObject['systolic-reading-2'],
        formDataObject['diastolic-reading-2'],
        formDataObject['pulse-reading-2']
      ],
      [
        formDataObject['systolic-reading-3'],
        formDataObject['diastolic-reading-3'],
        formDataObject['pulse-reading-3']
      ]
    ],
    "wbb":[
      formDataObject['wbb-1'],
      formDataObject['wbb-2'],
      formDataObject['wbb-3']
    ],
    "wab":[
      formDataObject['wab-1'],
      formDataObject['wab-2'],
      formDataObject['wab-3']
    ]
    };
    console.log("returnData is: ",returnData)
    let formDataJsonString = JSON.stringify(returnData);
    //Set the fetch options (headers, body)
    let fetchOptions = {
      //HTTP method set to POST.
      method: "PUT",
      //Set the headers that specify you're sending a JSON body request and accepting JSON response
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      // POST request body as JSON string.
      body: formDataJsonString,
    };
  
    //Get the response body as JSON.
    //If the response was not OK, throw an error.
    let res = await fetch(url, fetchOptions);
  
    //If the response is not ok throw an error (for debugging)
    if (!res.ok) {
      let error = await res.text();
      throw new Error(error);
    }
    //If the response was OK, return the response body.
    return res.json();
  }