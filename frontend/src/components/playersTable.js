
import './playersTable.css'

function PlayersTable(props){
    
    return (
        <div className="players-table">
            <table>
                <tr>
                    <th>Username</th>
                    <th>Bounty</th>
                </tr>
                {
                    props.players.map(element => {
                        return (
                            <tr key={element.id}>
                            <td>{element.username}</td>
                            <td>{element.bounty}</td>
                            </tr>
                        )
                    })
                }
            </table>
        </div>
    )
}

export {PlayersTable};
