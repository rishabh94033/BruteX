import { Stagehand } from "@browserbasehq/stagehand";
import { z } from "zod";

async function example() {
  const stagehand = new Stagehand({
    env: "LOCAL",
    verbose: 1,
    debugDom: true,
    enableCaching: true,
  });

  await stagehand.init(
    {
        modelName: "gpt-4o-mini",
        modelClientOptions: {
            baseURL: "https://models.inference.ai.azure.com"
        
        }
    }
  );
  await stagehand.page.goto("https://maitri.bmu.edu.in/login.htm");
  await stagehand.act({
    action: "fill in the form with %email% and %password% and submit",
    variables: {
      email: "",
      password: "",
    },
  });
  console.log("login initiated and returing")

  await stagehand.close();
}

(async () => {
  await example();
})();

