import { order_data } from "../generated-htmls/main-body.js";
console.log("loaded here now cccce", order_data)



function send_order_data(){
    return fetch("http://127.0.0.1:5000/data_api",{
        headers:{"Content-Type": "application/json"},
        method:"POST",
        body: JSON.stringify(order_data)
    })
        .then(response =>{
            if(!response.ok){
                throw new Error(`http status!${response.status} `)
            }
        })
        .then(data => console.log(data))
        .catch(error => console.error("failed to post order data", error))
    
}


function get_processed_orderDetails(){
    /**asumming all conditions explained in the final part are true! (ie under comment section), this function would be resposible for fetching order details data from the server side */
    return fetch("http://127.0.0.1:5000/data_api",
    {
        headers:{"Content-Type":"application/json"},
        method:"GET"
    }
    
    )
    .then(response =>{
        if(!response.ok){
            throw new Error(`http request status: ${response.status}`)
        }
        return response.json()
    })
    .then(data =>{
        const orderData = Array.isArray(data)?data:[data]
        return orderData
    })
    .catch(error => console.error("server did not send order details",error))
}


async function generateOrdered_productHtml(){
    try{
        await send_order_data()
    }
    catch(Error){
        console.error("http status: failed to send order data",error)
    }
    finally{
        /** this retrives the order details fetched from the server but i wont use it to generate the order html bcoz, it will generate for all order details in the database yet the focus is on the current client orders. this would be used if each time a client make orders, a new database for order details is dynamicly created. */


        // let in_comingData = await get_processed_orderDetails()
        // console.log("hahahah",in_comingData)


        let generated_chartlist= ""
        console.log("use this ",order_data)

        order_data.forEach((order)=> {
            generated_chartlist += `
                <div class="product-container">
                    <div class="image-section">
                        <img class="actual-image" src="${order["product_image"]}">
                    </div>

                    <div class="other-details">
                        <div>
                            Name: ${order["product_name"]}
                        </div>
                    </div>


                </<div>


                <div class="payment-container">
                
                    gthghujigtgryuiojhgfdrety
                
                </div>
            `


            
        });
        document.querySelector(".body-section")
            .innerHTML= generated_chartlist
    }
}



generateOrdered_productHtml()

