#ifndef UR3_BCI_H
#define UR3_BCI_H

#include <QWidget>
#include <ros/ros.h>

namespace Ui {
class UR3BCI;
}

class UR3BCI : public QWidget
{
  Q_OBJECT

public:
  explicit UR3BCI(QWidget *parent = nullptr);
  ~UR3BCI();

private:
  Ui::UR3BCI *ui;
};

#endif // UR3_BCI_H
