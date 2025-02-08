import Navbar from "./Navbar"

const MainLayout = ({ children }) => {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <div className="min-h-screen">
        {children}
      </div>
    </div>
  )
}

export default MainLayout;