class FoodCard extends React.Component {
  render() {
    return (
       <div className="col-lg-3 col-md-4 col-sm-6 portfolio-item">
          <div className="card card-inverse ">
            <a href={this.props.foods.id}><img className="card-img-top" src={this.props.foods.img} alt=""></img></a>
            <div className="overlay"> 
            </div>
            <div className="card-img-overlay over-title">
              <h4 className="card-title"><a href={this.props.foods.id}>{this.props.foods.name}</a></h4>
            </div>
            <div className="card-img-overlay">
              <p className="card-text">Calories: {this.props.foods.calories}</p>
              <p className="card-text">Fat: {this.props.foods.fat}</p>
            </div>
          </div>
        </div>
    );
  }
}

class Grid extends React.Component {
  constructor() {
    super();
    this.state = {
      foods: []
    }
  }
  
  componentWillMount() {
    // TODO: fill out array from database
    this.setState(
      {foods: [
        {
          id: 0,
          img: 'http://del.h-cdn.co/assets/17/23/1600x800/landscape-1497238977-delish-mason-jar-ice-cream-3.jpg', 
          name: 'Ice Cream', 
          calories: '137', 
          serving: '1/2 cup', 
          sodium: '53 mg', 
          fat: '7 g', 
          protein: '2.3 g'
        },
        {
          id: 1,
          img: 'http://baileysrestaurants.com/range/files/2013/02/IMG_1700.jpg', 
          name: 'Burger', 
          calories: '354', 
          serving: '1 item', 
          sodium: '497 mg', 
          fat: '17 g', 
          protein: '20 g'
        },
        {
          id: 2,
          img: 'http://catchyscoop.com/wp-content/uploads/2016/07/calories-in-a-waffle.jpg', 
          name: 'Waffle', 
          calories: '82', 
          serving: '1 oz', 
          sodium: '145 mg', 
          fat: '4 g', 
          protein: '2.2 g'
        }
      ]} 
    );
  }
  
  render() {
    let cards;
    cards = this.state.foods.map(food => {
      return (
        <FoodCard key={food.name} foods={food}/>
      );
    });
    return (
      <div className="row">
        {cards}
      </div>
    );
  }
}

ReactDOM.render(
  <Grid />,
  document.getElementById('food-grid')
);
