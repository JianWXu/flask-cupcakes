BASE_URL = "http://127.0.0.1:5000/api/cupcakes";
let flavor = $("#flavor").val();
let size = $("#size").val();
let rating = $("#rating").val();
let image = $("#image").val();
const $body = $("body");

$(".submit").submit(addCupcake);

async function addCupcake() {
  let data = {
    flavor,
    size,
    rating,
    image,
  };
  await axios({ url: BASE_URL, method: "post", data: data });
}

function generateCupcake(cupcake) {
  return $(
    `<li>${cupcake.flavor} <button class="delete-cupcake" data-id="${cupcake.id}">Delete</button></li>`
  );
}

async function putCupcakeInDiv() {
  const resp = await axios.get(BASE_URL);
  let cupcakes = resp.data.cupcakes;
  for (let cupcake of cupcakes) {
    $("#cupcake-ul").append(generateCupcake(cupcake));
  }
}

async function deleteCupcake() {
  const id = $(this).data("id");
  await axios.delete(`${BASE_URL}/${id}`);
  $(this).parent().remove();
}

$body.on("click", ".delete-cupcake", deleteCupcake);

putCupcakeInDiv();
