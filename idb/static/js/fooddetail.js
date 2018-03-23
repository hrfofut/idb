class FoodDetail extends React.Component {
  render() {
    return (
      <div>
        <h1 className="display-4">{this.props.name}</h1>
        <table class="table">
          <thead class="thead-light">
            <tr>
              <th scope="col" colspan="3">Nutritional Information</th>
            </tr>
            <tr>
              <th scope="row">Amount Per 1 serving</th>
              <th >{this.props.servings}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">Calories</th>
              <td>{this.props.calorie}</td>
            </tr>        
            <tr>
              <th scope="row">Sodium</th>
              <td>{this.props.sodium}</td>
            </tr>
            <tr>
              <th scope="row">Fat</th>
              <td>{this.props.fat}</td>
            </tr>
            <tr>
              <th scope="row">Protein</th>
              <td>{this.props.protein}</td>
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