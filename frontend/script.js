const form = document.getElementById("investmentForm");

const loading = document.getElementById("loading");
const results = document.getElementById("results");

const submitBtn = document.getElementById("submitBtn");

form.addEventListener("submit", async function (event) {
  event.preventDefault();

  loading.classList.remove("hidden");
  results.classList.add("hidden");

  submitBtn.disabled = true;

  const requestData = {
    age: Number(document.getElementById("age").value),

    goal: document.getElementById("goal").value,

    horizon: Number(document.getElementById("horizon").value),

    income: Number(document.getElementById("income").value),

    risk: document.getElementById("risk").value,
  };

  try {
    const response = await fetch("/api/invest", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(requestData),
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status}`);
    }

    const data = await response.json();

    /* ================= PROFILE ================= */

    document.getElementById("profileAge").textContent = data.profile.age;

    document.getElementById("profileGoal").textContent = data.profile.goal;

    document.getElementById("profileHorizon").textContent =
      `${data.profile.horizon} Years`;

    document.getElementById("profileIncome").textContent = `₹${Number(
      data.profile.income,
    ).toLocaleString("en-IN")}`;

    /* ================= RISK ================= */

    document.getElementById("riskLevel").textContent = data.risk.level;

    document.getElementById("riskScore").textContent = data.risk.score;

    document.getElementById("riskExplanation").textContent =
      data.risk.explanation;

    /* ================= ALLOCATION ================= */

    const stocks = data.allocation.stocks;

    const bonds = data.allocation.bonds;

    const gold = data.allocation.gold;

    const cash = data.allocation.cash;

    document.getElementById("stocks").textContent = `${stocks}%`;

    document.getElementById("bonds").textContent = `${bonds}%`;

    document.getElementById("gold").textContent = `${gold}%`;

    document.getElementById("cash").textContent = `${cash}%`;

    setTimeout(() => {
      document.getElementById("stocksBar").style.width = `${stocks}%`;

      document.getElementById("bondsBar").style.width = `${bonds}%`;

      document.getElementById("goldBar").style.width = `${gold}%`;

      document.getElementById("cashBar").style.width = `${cash}%`;
    }, 100);

    document.getElementById("allocationSummary").textContent =
      data.summary.allocation;

    /* ================= ETFs ================= */

    const etfContainer = document.getElementById("etfContainer");

    etfContainer.innerHTML = "";

    data.etfs.forEach((etf) => {
      const div = document.createElement("div");

      div.className = "etf-card";

      let marketPrice = "Market data unavailable";

      if (data.market_data && data.market_data[etf.ticker]) {
        const prices = data.market_data[etf.ticker];

        const dates = Object.keys(prices);

        if (dates.length > 0) {
          const latestDate = dates[dates.length - 1];

          const latestPrice = prices[latestDate];

          marketPrice = `$${latestPrice} (${latestDate})`;
        }
      }

      div.innerHTML = `

                <div class="etf-top">

                    <span class="etf-ticker">
                        ${etf.ticker}
                    </span>

                    <span class="etf-class">
                        ${etf.asset_class}
                    </span>

                </div>


                <h3>
                    ${etf.name}
                </h3>


                <p>
                    ${etf.reason}
                </p>


                <div class="etf-price">

                    Latest Price:

                    <strong>
                        ${marketPrice}
                    </strong>

                </div>

            `;

      etfContainer.appendChild(div);
    });

    /* ================= SUMMARY ================= */

    document.getElementById("investorSummary").textContent =
      data.summary.investor;

    document.getElementById("etfSummary").textContent = data.summary.etfs;

    document.getElementById("disclaimer").textContent = data.summary.disclaimer;

    /* ================= SHOW RESULTS ================= */

    results.classList.remove("hidden");

    results.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  } catch (error) {
    console.error(error);

    alert(
      "Something went wrong while analyzing your investment profile. Please check the terminal for details.",
    );
  } finally {
    loading.classList.add("hidden");

    submitBtn.disabled = false;
  }
});
