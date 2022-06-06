pragma solidity ^0.6.0;

contract MacroToken {
    string  public name = "Macro Token";
    string  public symbol = "MCR";
    uint256 public totalSupply = 100000000 * 10 ** 18;
    uint8   public decimals = 18;
    uint public rate = 10000;
    uint public amount_sold = 0;
    uint256 public amount_sold_limit = 50000000 * 10 ** 18;
    address public owner;
    bool locked = true;

    event TokensPurchased(
        address account,
        address token,
        uint amount,
        uint rate
    );
    event Transfer(
        address indexed _from,
        address indexed _to,
        uint256 _value
    );

    event Approval(
        address indexed _owner,
        address indexed _spender,
        uint256 _value
    );

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    constructor() public {
        balanceOf[address(this)] = totalSupply;
        owner = msg.sender;
    }
    
    function getBalance(address _owner) public view returns(uint) {
        return balanceOf[_owner];
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(locked == false, "Liquidity is still locked. Transfer of tokens is not allowed");
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(locked == false, "Liquidity is still locked. Transfer of tokens is not allowed");
        require(_value <= balanceOf[_from]);
        require(_value <= allowance[_from][msg.sender]);
        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        allowance[_from][msg.sender] -= _value;
        emit Transfer(_from, _to, _value);
        return true;
    }
    function getRate() public view returns(uint) {
        return rate;
    }
    function getCurrentPresaleSales() public view returns(uint) {
        return amount_sold;
    }
    function getCurrentPresaleLimit() public view returns(uint) {
        return amount_sold_limit;
    }
    function burn() public {
        require(msg.sender == owner, "Only the owner can burn the tokens");
        balanceOf[address(this)] -= 10000 *10** 18;
        balanceOf[address(0x000000000000000000000000000000000000dEaD)] += 10000*10** 18;
    }

    function changeRate(uint _rate, uint _limit) public {
        require(msg.sender == owner, "Only the owner can change the rates");
        amount_sold = 0;
        rate = _rate;
        amount_sold_limit = _limit * 10 ** 18;
    }
 
    function buyTokens() public payable {
        uint tokenAmount = msg.value * rate;
        require(tokenAmount+amount_sold < amount_sold_limit, "You can't buy this much for now. Try buying less or wait till the next presale.");
        require(getBalance(address(this)) >= tokenAmount, "Contract doesnt have enough tokens");
        balanceOf[address(this)] -= tokenAmount;
        balanceOf[msg.sender] += tokenAmount;
        amount_sold += tokenAmount;
        emit TokensPurchased(msg.sender, address(this), tokenAmount, rate);
    }
    
    function withdraw() public {
        require(msg.sender == owner, "only owner can unlock the liquidity");
        require(block.timestamp >= 1664578800, "too early to unlock the liquidity");
        locked = false;
        payable(owner).transfer(address(this).balance);
    }

}