import { faCircleNotch } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"

const Loader = () => {
    return <FontAwesomeIcon className="animate-spin w-12 h-12 text-amber-700/75" icon={faCircleNotch} />
}

export default Loader