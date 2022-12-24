#include "ur3_bci.h"
#include "ui_ur3_bci.h"

UR3BCI::UR3BCI(QWidget *parent) :
  QWidget(parent),
  ui(new Ui::UR3BCI)
{
  ui->setupUi(this);
}

UR3BCI::~UR3BCI()
{
  delete ui;
}
