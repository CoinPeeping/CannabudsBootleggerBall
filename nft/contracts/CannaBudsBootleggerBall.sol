// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract CannaBudsBootleggerBall is ERC721, Ownable {
    
    uint256 public constant MAX_SUPPLY = 10420;
    uint256 public constant MAX_PURCHASABLE = 20;

    uint256 public tokenPrice = 42000000000000000; // 0.0420 ETH
    
    bool public saleIsActive = false;
    bool public whitelistActive = false;

    address[] public whitelistedAddresses;

    constructor(string memory name, string memory symbol, string memory _baseURI)  public
    ERC721(name, symbol){
        setBaseURI(_baseURI);
        reserveTokens(5);
    }

    // SETTER FUNCTIONS

    function openSale() public onlyOwner {
        saleIsActive = true;
    }

    function closeSale() public onlyOwner {
        saleIsActive = false;
    }

    function openWhitelist() public onlyOwner {
        whitelistActive = true;
    }

    function closeWhitelist() public onlyOwner {
        whitelistActive = false;
    }

    function setBaseURI(string memory _baseURI) public onlyOwner {
        _setBaseURI(_baseURI);
    }

    function setTokenPrice(uint256 _newPrice) public onlyOwner {
        tokenPrice = _newPrice;
    }

    // GETTERS

    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
        string memory baseURI = baseURI();
        return bytes(baseURI).length > 0 ? string(abi.encodePacked(baseURI, tokenId.toString())) : "";
    }

    // MINTING FUNCTIONS

    function presaleMint(uint256 numberOfTokens) public payable {
        require(isWhitelisted(msg.sender), "You must be on the whitelist to mint during the presale.");
        require(balanceOf(msg.sender).add(numberOfTokens) <= 10, "You can only mint 10 before the sale begins");
        require(numberOfTokens > 0, "Minimum mint is 1 token");
        require(numberOfTokens <= 10, "You can only mint up to 10 tokens during the presale.");
        require(saleIsActive && whitelistActive, "Sale and whitelist must be active to mint");
        require(tokenPrice.mul(numberOfTokens) <= msg.value, "Incorrect Ether value.");

        for (uint256 i = 0; i < numberOfTokens; i++) {
            uint256 mintIndex = totalSupply();
            _safeMint(msg.sender, mintIndex);
        }
    }

    function mint(uint256 numberOfTokens) public payable {
        require(saleIsActive, "Sale is not active.");
        require(totalSupply() < MAX_SUPPLY, "All tokens have been minted.");
        require(totalSupply() + numberOfTokens <= MAX_SUPPLY, "The amount of tokens you are trying to mint exceeds the max supply.");
        require(numberOfTokens > 0, "Minimum mint is 1 token");
        require(numberOfTokens <= MAX_PURCHASABLE, "Maximum mint is 20 tokens");
        require(tokenPrice.mul(numberOfTokens) <= msg.value, "Incorrect Ether value.");
        require(!whitelistActive, "Only whitelisted users may mint at this time");

        for (uint256 i = 0; i < numberOfTokens; i++) {
            uint256 mintIndex = totalSupply();
            _safeMint(msg.sender, mintIndex);
        }
    }

    function reserveTokens(uint256 _reserveAmount) public onlyOwner {        
        uint supply = totalSupply();

        require(
            _reserveAmount > 0 && _reserveAmount + supply <= MAX_SUPPLY,
            "Not enough reserve left for team"
        );

        for (uint256 i = 0; i < _reserveAmount; i++) {
            _safeMint(msg.sender, supply + i);
        }
    }

    function withdraw() public payable onlyOwner {
        require(payable(msg.sender).send(address(this).balance));
    }

    // WHITELIST METHODS

    function addToWhitelist(address[] calldata _users) public onlyOwner {
        delete whitelistedAddresses;
        whitelistedAddresses = _users;
    }

    function isWhitelisted(address _user) public view returns (bool){
        for (uint i = 0; i < whitelistedAddresses.length; i++) {
            if(whitelistedAddresses[i] == _user){
                return true;
            }
        }
        return false;
    }

    function clearWhitelist() public onlyOwner {
        delete whitelistedAddresses;
    }

    function getWhitelistSize() public view returns (uint256){
        return whitelistedAddresses.length;
    }


}