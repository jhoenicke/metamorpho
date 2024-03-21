// SPDX-License-Identifier: GPL-2.0-or-later
import "ConsistentState.spec";

using MorphoHavoc as M;

methods {
    function _.supply(MetaMorphoHarness.MarketParams marketParams, uint256 assets, uint256 shares, address onBehalf, bytes data) external => summarySupply(marketParams, assets, shares, onBehalf, data) expect (uint256, uint256) ALL;
    function _.withdraw(MetaMorphoHarness.MarketParams marketParams, uint256 assets, uint256 shares, address onBehalf, address receiver) external => summaryWithdraw(marketParams, assets, shares, onBehalf, receiver) expect (uint256, uint256) ALL;
    function _.idToMarketParams(MetaMorphoHarness.Id id) external => summaryIdToMarketParams(id) expect MetaMorphoHarness.MarketParams ALL;

    function M.libId(MetaMorphoHarness.MarketParams marketParams) external returns(MetaMorphoHarness.Id) envfree;
}

function summaryIdToMarketParams(MetaMorphoHarness.Id id) returns MetaMorphoHarness.MarketParams {
    MetaMorphoHarness.MarketParams marketParams;

    // Safe require because:
    // - markets in the supply/withdraw queue have positive lastUpdate (see LastUpdated.spec)
    // - lastUpdate(id) > 0 => marketParams.id() == id is a verified invariant in Morpho Blue.
    require M.libId(marketParams) == id;

    return marketParams;
}

function summarySupply(MetaMorphoHarness.MarketParams marketParams, uint256 assets, uint256 shares, address onBehalf, bytes data) returns(uint256, uint256) {
    assert shares == 0;
    assert onBehalf == currentContract;
    assert data.length == 0;

    MetaMorphoHarness.Id id = M.libId(marketParams);
    // Safe require because it is a verified invariant
    require hasSupplyCapIsEnabled(id);

    // Check that all markets on which MetaMorpho supplies are enabled markets.
    assert config_(id).enabled;

    // NONDET summary, which is sound because all non view functions in Morpho Blue are abstracted away.
    return (_, _);
}

function summaryWithdraw(MetaMorphoHarness.MarketParams marketParams, uint256 assets, uint256 shares, address onBehalf, address receiver) returns (uint256, uint256) {
    assert onBehalf == currentContract;
    assert receiver == currentContract;

    MetaMorphoHarness.Id id = M.libId(marketParams);
    uint256 rank = withdrawRank(id);
    // Safe require because it is a verified invariant.
    require isInWithdrawQueueIsEnabled(assert_uint256(rank - 1));
    // Safe require because it is a verified invariant
    require isWithdrawRankCorrect(id);

    // Check that all markets from which MetaMorpho withdraws are enabled markets.
    assert config_(id).enabled;

    // NONDET summary, which is sound because all non view functions in Morpho Blue are abstracted away.
    return (_, _);
}

invariant checkSummaries()
    true;
