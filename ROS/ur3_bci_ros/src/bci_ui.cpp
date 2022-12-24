#include <QApplication>
#include "ur3_bci.h"

int main(int argc, char *argv[]){
  ros::init(arc, argv, "ur3_bci_ui_node", ros::init_options::AnonymousName);
  QApplication a(argc, argv);

  UR3BCI w;
  w.setWindowTitle(QString::fromStdString(ros::this_node::getName()));
  w.show();
  return a.exec();
}
