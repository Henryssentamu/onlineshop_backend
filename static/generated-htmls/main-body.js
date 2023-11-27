let update_data = [];

function fetchData() {

    return fetch("http://127.0.0.1:5000/product_details", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
    })
        .then((response) => {
        if (!response.ok) {
            throw new Error(`http error status: ${response.status}`);
        }
        return response.json();
        })
        .then((data) => {
            const dataArray = Array.isArray(data)? data: [data];
            return dataArray
        })
        .catch((error) => console.error("error", error));
    }







async function updateDataAndGenerateHtml() {
    let generated_main_html = "";
    try {
        // Wait for fetchData to complete
        const data = await fetchData()

        data.forEach((product)=>{
            generated_main_html += `
                <div class=" product-container"> 
                    <div class="product-image-section">


                        <!-- THIS LINK SHOULD TAKE YOU TO THE PRODUCT DETAILS PAGE ON CLICK IN THE IMAGE.. AND IT IS TO BE DONE IN THE BACKEND -->


                        <a class="image-link" href="{{url_for('#')}}">
                            <img  class="product-image" src="${product.image}">  
                        </a>
                    </div>



                    <div class="details-container">
                        <div class=" product-name">
                            Name: ${product.name}
                        </div>
                        <div class="shopping-details">
                            <div class="product-price">
                                Price: $ ${(product.price/100).toFixed(2)}
                            </div>
                            <div class="select-qantity">    
                                <!-- the function brings error on accessing current qantity. there i used select element direct -->

                                <select class = "selectQantity-${product.productId}">
                                    <option value = "1"> 1 </option>
                                    <option value = "2"> 2 </option>
                                    <option value = "3"> 3 </option>
                                    <option value = "4"> 4 </option>
                                    <option value = "5"> 5 </option>
                                    <option value = "6"> 6 </option>
                                    <option value = "7"> 7 </option>
                                    <option value = "8"> 8 </option>
                                    <option value = "9"> 9 </option>
                                    <option value = "10"> 10 </option>
                                </select>                  
                            
                            </div>
                        </div>
                    </div>
                    <div class=" added-to-chart-notification-css  added-to-chart-notification_${product.productId}"></div>

                    <div class="button-section">
                        <button  data-product-id="${product.productId}" data-product-name="${product.name}" data-product-image="${product.image}"class="add-to-chart-button"> add to chart </button>
                    </div>

                    


                </div>
            `
        })

        document.querySelector(".main_body_section")
            .innerHTML = generated_main_html;

        /** this function activates other DOM section which makes the site interactive  */
        makeSiteInteractive();

    }
    catch (error) {
    console.error("error! failed to fetch data", error);}

}

// Call the function to fetch data and generate HTML
updateDataAndGenerateHtml()
let orderDetails = []




function makeSiteInteractive(){
    
    

    document.querySelectorAll(".add-to-chart-button")
        .forEach((button)=>{
            button.addEventListener("click",()=>{
                let productId = button.dataset.productId
                let productImage = button.dataset.productImage
                let productName = button.dataset.productName
                console.log(productId)
                

                /** notification for the added data */

                document.querySelector(`.added-to-chart-notification_${productId}`).innerHTML = "added to chart";
                /** updating the order figure  in the chart section */
                numberOfOrders()
                let qantityOfOrderedProduct = getCurrentQantity(productId)
                let deliver_to = getDeliveryLocation()
                

                orderDetails.push({"product_Id":productId,"ordered_Qantity":qantityOfOrderedProduct, "DeliveryTo":deliver_to,"product_name":productName, "product_image":productImage})
                localStorage.setItem("order_data",JSON.stringify(orderDetails))
                

            })
        })
    


}






function numberOfOrders(){
    /** this function finds and update number of orders in the chart  on click*/

    /** getting the current number  */

    let currentOrderNumber = Number(document.querySelector(".number-of-orders").innerHTML)

    /** updating it  */

    document.querySelector(".number-of-orders")
        .innerHTML = currentOrderNumber + 1  
    

}



function getCurrentQantity(id){
    /** a function returns the current qantity selected */

    let currentQantity = document.querySelector(`.selectQantity-${id}`).value
    return currentQantity;
    
}

function getDeliveryLocation(){
    /** this function gets the location to deliver the product */
    let location = document.querySelector(".select").value
    return location
}


export let order_data = JSON.parse(localStorage.getItem("order_data"))





























































// fetch("http://127.0.0.1:5000/product_details",
//     {
//         method:"GET",
//         headers: {"Content-Type":"application/json"}
//     })
//     .then(response =>{
//         if (!response.ok){
//             throw new Error(`http error status: ${response.status}`)
//         }
//         return response.json()
//     })
//     .then(data =>{
//                         data.forEach((productArray)=>{
//                             // console.log("test pro",productArray)
//                             update_data.push(productArray)
//                         })
//                         //console.log("product details container:",data);

//                 })
//     .catch(error => console.error("error",error))
























/** afunction which create select element dynamically with different options  *

export function qantity_selection(Id){
   let selectElement = document.createElement("select")
   selectElement.className = `selectQantity-${Id}`
   console.log(selectElement.className)
   for(let i =1; i<= 10; i++){
    let options = document.createElement("option")
    options.value = i;
    options.text = i;
    selectElement.appendChild(options);

   }
   return selectElement
   
}*/














