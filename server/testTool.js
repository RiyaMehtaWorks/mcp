import { toolRegistry } from "./tools/index.js";

async function test() {
  const result = await toolRegistry.pythonSearch({
    query:"fertilizer for wheat",
    state:"Haryana",
    crop: "Wheat"
  });
//   console.log(result);
console.log(JSON.stringify(result, null, 2));
}

test();