class FoodDetail extends React.Component {
  render() {
    return (
      <div>
        <h1 className="display-4"><a href="https://www.google.com/search?q=">{this.props.name}</a></h1>
        <table class="table">
          <thead class="thead-light">
            <tr>
              <th scope="col" colspan="3">Nutritional Information</th>
            </tr>
            <tr>
              <th scope="row">Amount Per 1 serving</th>
              <th >{this.props.servings} g</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">Calories</th>
              <td>{this.props.calorie} kCal</td>
            </tr>        
            <tr>
              <th scope="row">Sodium</th>
              <td>{this.props.sodium} mg</td>
            </tr>
            <tr>
              <th scope="row">Fat</th>
              <td>{this.props.fat} g</td>
            </tr>
            <tr>
              <th scope="row">Protein</th>
              <td>{this.props.protein} g</td>
            </tr>
          </tbody>
        </table>
      </div>
    );
  }
}

ReactDOM.render(
  <FoodDetail name={document.getElementById('food-detail').getAttribute('name')}
  servings={document.getElementById('food-detail').getAttribute('servings')} 
  calorie={document.getElementById('food-detail').getAttribute('calorie')} 
  sodium={document.getElementById('food-detail').getAttribute('sodium')}
  fat={document.getElementById('food-detail').getAttribute('fat')} 
  protein={document.getElementById('food-detail').getAttribute('protein')}  />,
  document.getElementById('food-detail')
);