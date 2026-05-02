import { toolRegistry } from "./tools/index.js";

async function test() {
  const result = await toolRegistry.pythonSearch({
    query:"rice pests",
    state:"Punjab",
    crop: "Rice"
  });
  console.log(result);
}

test();