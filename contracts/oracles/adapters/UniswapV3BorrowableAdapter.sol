// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import {IUniswapV3Pool} from "@uniswap/v3-core/interfaces/IUniswapV3Pool.sol";

import {OracleFeed} from "../libraries/OracleFeed.sol";
import {UniswapV3PoolLib} from "../libraries/UniswapV3PoolLib.sol";

import {BaseOracle} from "../BaseOracle.sol";

abstract contract UniswapV3BorrowableAdapter is BaseOracle {
    using UniswapV3PoolLib for IUniswapV3Pool;

    IUniswapV3Pool internal immutable UNI_V3_BORROWABLE_POOL;
    uint32 internal immutable UNI_V3_BORROWABLE_DELAY;

    constructor(address pool, uint32 delay) {
        UNI_V3_BORROWABLE_POOL = IUniswapV3Pool(pool);
        UNI_V3_BORROWABLE_DELAY = delay;
    }

    function BORROWABLE_FEED() external view returns (string memory, address) {
        return (OracleFeed.UNISWAP_V3, address(UNI_V3_BORROWABLE_POOL));
    }

    function borrowableScale() public view virtual override returns (uint256) {
        return 1e18;
    }

    function borrowableToBasePrice() public view virtual override returns (uint256) {
        return UNI_V3_BORROWABLE_POOL.price(UNI_V3_BORROWABLE_DELAY);
    }
}
